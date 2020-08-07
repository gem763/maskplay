from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
# from vote.models import VoteModel
from siteflags.models import ModelWithFlag, FlagBase
from datetime import datetime
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.db.models import Q

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
import json
import os


VOTE_UP = 0
VOTE_DOWN = 1
FOLLOW = 10


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class Flager(FlagBase):
    user = models.ForeignKey('Boo', related_name='%(class)s_users', verbose_name='Boo', on_delete=models.CASCADE)


class User(AbstractEmailUser):
    boo_selected = models.IntegerField(default=0)

    @property
    def boo(self):
        return Boo.objects.get(pk=self.boo_selected, user=self)

    @property
    def serialized(self):
        _user = UserSerializer([self], many=True).data[0]
        _user['boos'] = {boo.pop('id'):boo for boo in _user['boos']}
        return json.dumps(_user)

    def set_boo(self, boo_id):
        self.boo_selected = boo_id
        self.save()


def _profilepix_path(instance, fname):
    user = instance.boo.user.email
    fname = str(datetime.now()) + '__' + fname
    fmt = 'user/{user}/{fname}'
    return fmt.format(user=user, fname=fname)


def _maskpix_path(instance, fname):
    fname = str(datetime.now()) + fname
    fmt = 'mask/{type}/{category}/{fname}'
    return fmt.format(fname=fname, type=instance.type.lower(), category=instance.category)


class MaskBase(BigIdAbstract):
    MASK_TYPES = ( ('EYE', 'eye'), ('MOUTH', 'mouth') )

    type = models.CharField(max_length=5, choices=MASK_TYPES, default='EYE')
    category = models.CharField(max_length=50, null=False, blank=False, default='base')
    pix = models.ImageField(upload_to=_maskpix_path, max_length=500, null=False, blank=False)

    def __str__(self):
        return self.type + ' | ' + self.category + ' | ' + os.path.basename(self.pix.name)


class Mask(BigIdAbstract):
    maskbase = models.ForeignKey(MaskBase, null=False, blank=False, on_delete=models.CASCADE)
    top = models.FloatField(default=0, null=False, blank=False)
    left = models.FloatField(default=0, null=False, blank=False)
    width = models.FloatField(default=100, null=False, blank=False)
    height = models.FloatField(default=20, null=False, blank=False)

    def __str__(self):
        fmt = '{maskbase} | T={top}, L={left}, W={width}, H={height}'
        return fmt.format(maskbase=self.maskbase, top=self.top, left=self.left, width=self.width, height=self.height)


class Profile(BigIdAbstract):
    PROFILE_TYPES = ( ('IMAGE', 'image'), ('TEXT', 'text') )

    type = models.CharField(max_length=5, choices=PROFILE_TYPES, default='IMAGE', null=False, blank=False)
    # boo = models.ForeignKey(Boo, on_delete=models.CASCADE)
    pix = models.ImageField(upload_to=_profilepix_path, max_length=500, null=False, blank=False)
    image = models.ImageField(upload_to=_profilepix_path, max_length=500, null=True, blank=True)
    text = models.CharField(max_length=10, null=True, blank=True)
    eye_mask = models.OneToOneField(Mask, null=True, blank=True, on_delete=models.SET_NULL, related_name='eye')
    mouth_mask = models.OneToOneField(Mask, null=True, blank=True, on_delete=models.SET_NULL, related_name='mouth')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type + ' | ' + os.path.basename(self.pix.name)

    @property
    def serialized(self):
        _profile = ProfileSerializer([self], many=True).data[0]
        return json.dumps(_profile)


class Boo(BigIdAbstract, ModelWithFlag):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100)
    text = models.TextField(max_length=200, blank=True, null=True)
    # profile_selected = models.IntegerField(default=0)
    profile = models.OneToOneField(Profile, null=True, blank=True, on_delete=models.SET_NULL) # SET_NULL을 미리정의된 프로파일로 교체하게 만들어야한다...
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nick + ' | ' + self.user.email

    @property
    def serialized(self):
        _boo = BooSerializer([self], many=True).data[0]
        return json.dumps(_boo)

    # @property
    # def profile(self):
    #     return Profile.objects.get(pk=self.profile_selected, boo=self)

    def follow(self, boo_id, note=None):
        boo = Boo.objects.get(pk=boo_id)
        boo.set_flag(self, note=note, status=FOLLOW)

    def unfollow(self, boo_id):
        boo = Boo.objects.get(pk=boo_id)
        boo.remove_flag(self, status=FOLLOW)

    def is_following(self, boo_id):
        boo = Boo.objects.get(pk=boo_id)
        return boo.is_flagged(self, status=FOLLOW)

    @property
    def is_followed(self):
        myboo = get_current_user().boo
        return myboo.is_following(self.id)

    @property
    def followers_id(self):
        return list(self.get_flags(status=FOLLOW).values_list('user_id', flat=True))

    @property
    def followees_id(self):
        return list(Flager.objects.filter(status=FOLLOW, user=self).values_list('object_id', flat=True))

    @property
    def followers(self):
        return Boo.objects.filter(id__in=self.followers_id)
        # return [f.user for f in self.get_flags(status=self.FLAG_FOLLOW)]

    @property
    def followees(self):
        return Boo.objects.filter(id__in=self.followees_id)
        # boo_ids = Flager.objects.filter(status=self.FLAG_FOLLOW, user=self).values_list('object_id', flat=True)
        # return Boo.objects.filter(id__in=boo_ids)

    @property
    def nfollowers(self):
        return len(self.followers_id)

    @property
    def nfollowees(self):
        return len(self.followees_id)

    @property
    def voting_record(self):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return {f.object_id:f.status for f in Flager.objects.filter(q, user=self)}



class Post(BigIdAbstract, ModelWithFlag):#, VoteModel):
    boo = models.ForeignKey(Boo, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()

    def __str__(self):
        return self.boo.nick + ' | ' + str(self.created_at)

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def vote(self, action, boo=None):
        if boo is None:
            boo = get_current_user().boo

        # up
        if action==VOTE_UP:
            self.set_flag(boo, status=VOTE_UP)
            self.remove_flag(boo, status=VOTE_DOWN)

        # down
        elif action==VOTE_DOWN:
            self.remove_flag(boo, status=VOTE_UP)
            self.set_flag(boo, status=VOTE_DOWN)

        # clear
        else:
            self.remove_flag(boo, status=VOTE_UP)
            self.remove_flag(boo, status=VOTE_DOWN)

    @property
    def voters(self):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return Flager.objects.filter(q)

    @property
    def nvotes_up(self):
        return Flager.objects.filter(status=VOTE_UP, object_id=self.id).count()

    @property
    def nvotes_down(self):
        return Flager.objects.filter(status=VOTE_DOWN, object_id=self.id).count()


def _postpix_path(instance, fname):
    user = instance.boo.user.email
    now = datetime.now()
    fname = str(now) + '__' + fname
    fmt = 'post/{year}/{month}/{day}/{user}/{fname}'
    return fmt.format(year=now.year, month=now.month, day=now.day, user=user, fname=fname)


class PostVoteOX(Post):
    pix = models.ImageField(upload_to=_postpix_path, max_length=500, null=True, blank=True)

    def __str__(self):
        return 'OX | ' + self.boo.nick


class PostVoteAB(Post):
    pix_a = models.ImageField(upload_to=_postpix_path, max_length=500, null=True, blank=True)
    pix_b = models.ImageField(upload_to=_postpix_path, max_length=500, null=True, blank=True)

    def __str__(self):
        return 'AB | ' + self.boo.nick



# class FollowSerializer(serializers.ModelSerializer):
#     profile = serializers.CharField(source='profile.pix.url')
#
#     class Meta:
#         model = Boo
#         fields = ['id', 'profile']
#         read_only_fields = fields

class MaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mask
        fields = ['id', 'maskbase', 'top', 'left', 'width', 'height']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    eye_mask = MaskSerializer()
    mouth_mask = MaskSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'type', 'eye_mask', 'mouth_mask', 'pix', 'pix_base', 'txt']
        read_only_fields = fields


class BooSerializer(serializers.ModelSerializer):
    # followers = FollowSerializer(many=True)
    # followees = FollowSerializer(many=True)
    # profile2 = serializers.CharField(source='profile.pix.url')
    profile = ProfileSerializer()

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'followers_id', 'followees_id', 'profile', 'voting_record']
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    boos = BooSerializer(source='boo_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'boo_selected', 'boos']
        read_only_fields = fields


# https://stackoverflow.com/questions/39104575/django-rest-framework-recursive-nested-parent-serialization
# class BooSerializer(serializers.ModelSerializer):
#     followers = serializers.SerializerMethodField()
#     # followees = SerializerMethodField(many=True)
#     profile = serializers.CharField(source='profile.pix.url')
#
#     class Meta:
#         model = Boo
#         fields = ['id', 'nick', 'text', 'followers', 'profile']
#         read_only_fields = fields
#
#     def get_followers(self, obj):
#         if len(obj.followers)==0:
#             return None
#         else:
#             # return BooSerializer(obj.followers, many=True).data
#             return FollowSerializer(obj.followers, many=True).data
