from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
from vote.models import VoteModel
from siteflags.models import ModelWithFlag, FlagBase
from datetime import datetime
from django_currentuser.middleware import get_current_user, get_current_authenticated_user

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
import json


# Create your models here.

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

    # @property
    # def boos(self):
    #     _boos = BooSerializer(self.boo_set, many=True).data
    #     _boos = {boo.pop('id'):boo for boo in _boos}
    #     return json.dumps(_boos)

    @property
    def serialized(self):
        _user = UserSerializer([self], many=True).data[0]
        _user['boos'] = {boo.pop('id'):boo for boo in _user['boos']}
        return json.dumps(_user)

    def set_boo(self, boo_id):
        self.boo_selected = boo_id
        self.save()



class Boo(BigIdAbstract, ModelWithFlag):
    FLAG_FOLLOW = 10

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100)
    text = models.TextField(max_length=500, blank=True, null=True)
    profile_selected = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nick + ' | ' + self.user.email

    @property
    def profile(self):
        return Profile.objects.get(pk=self.profile_selected, boo=self)

    def follow(self, boo_id, note=None):
        boo = Boo.objects.get(pk=boo_id)
        boo.set_flag(self, note=note, status=boo.FLAG_FOLLOW)

    def unfollow(self, boo_id):
        boo = Boo.objects.get(pk=boo_id)
        boo.remove_flag(self, status=boo.FLAG_FOLLOW)

    def is_following(self, boo_id):
        boo = Boo.objects.get(pk=boo_id)
        return boo.is_flagged(self, status=boo.FLAG_FOLLOW)

    @property
    def is_followed(self):
        myboo = get_current_user().boo
        return myboo.is_following(self.id)

    @property
    def followers_id(self):
        return list(self.get_flags(status=self.FLAG_FOLLOW).values_list('user_id', flat=True))

    @property
    def followees_id(self):
        return list(Flager.objects.filter(status=self.FLAG_FOLLOW, user=self).values_list('object_id', flat=True))

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


def _profilepix_path(instance, fname):
    user = instance.boo.user.email
    fname = str(datetime.now()) + '__' + fname
    fmt = 'user/{user}/{fname}'
    return fmt.format(user=user, fname=fname)


class Profile(BigIdAbstract):
    boo = models.ForeignKey(Boo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    pix = models.ImageField(upload_to=_profilepix_path, max_length=500, null=True, blank=True)

    def __str__(self):
        return self.boo.nick + ' | ' + self.boo.user.email


class Post(BigIdAbstract, VoteModel):
    boo = models.ForeignKey(Boo, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()

    def __str__(self):
        return self.boo.nick + ' | ' + str(self.created_at)

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def vote(self, action, boo_id):
        # up
        if action==0:
            self.votes.up(boo_id)

        # down
        elif action==1:
            self.votes.down(boo_id)

    # def voted_up(self, boo_id):
    #     return self.votes.exists(boo_id, action=0)
    #
    # def voted_down(self, boo_id):
    #     return self.votes.exists(boo_id, action=1)

    # def voted(self, boo_id):
    #     if self.votes.exists(boo_id, action=0):
    #         return 0
    #
    #     elif self.votes.exists(boo_id, action=1):
    #         return 1
    #
    #     else:
    #         return None

    @property
    def voted(self):
        boo_id = get_current_user().boo.pk

        if self.votes.exists(boo_id, action=0):
            return 0

        elif self.votes.exists(boo_id, action=1):
            return 1

        else:
            return None


    @property
    def nvotes(self):
        return self.num_vote_up + self.num_vote_down

    # def score(self, what, alpha=0, beta=0):
    #     try:
    #         if what=='up':
    #             num_vote = self.num_vote_up + alpha
    #
    #         elif what=='down':
    #             num_vote = self.num_vote_down + alpha
    #
    #         nvotes = self.nvotes + beta
    #         return int(num_vote / nvotes * 100)
    #
    #     except:
    #         return 0
    #
    # @property
    # def score_up(self):
    #     return self.score('up')
    #
    # @property
    # def score_down(self):
    #     return self.score('down')
    #
    # @property
    # def score_up_new(self):
    #     return self.score('up', alpha=1, beta=1)
    #
    # @property
    # def score_down_new(self):
    #     return self.score('down', alpha=1, beta=1)
    #
    # @property
    # def score_up_change(self):
    #     return self.score('up', alpha=1)
    #
    # @property
    # def score_down_change(self):
    #     return self.score('down', alpha=1)


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


class BooSerializer(serializers.ModelSerializer):
    # followers = FollowSerializer(many=True)
    # followees = FollowSerializer(many=True)
    profile = serializers.CharField(source='profile.pix.url')

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'followers_id', 'followees_id', 'profile']
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
