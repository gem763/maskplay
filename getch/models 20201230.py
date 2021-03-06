from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
# from vote.models import VoteModel
from siteflags.models import ModelWithFlag, FlagBase
from datetime import datetime
from django.conf import settings
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from IPython.core.debugger import set_trace
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
import json
import os


VOTE_UP = 0
VOTE_DOWN = 1
FOLLOW = 10
LIKE_COMMENT = 100

BOO_DELETED = 97


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class Flager(FlagBase):
    user = models.ForeignKey('Boo', related_name='%(class)s_users', verbose_name='Boo', on_delete=models.CASCADE)


class Styletag(BigIdAbstract):
    tag = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.tag


class Fashiontem(BigIdAbstract):
    item = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.item


class User(AbstractEmailUser):
    # email = models.EmailField(_('email address'), max_length=255, unique=False, db_index=True)
    boo_selected = models.IntegerField(default=0)

    @property
    def boo(self):
        return Boo.objects.get(pk=self.boo_selected, user=self)

    @property
    def other_boos(self):
        _boos = Boo.objects.filter(user=self).exclude(pk=self.boo_selected)
        _boos = BooSerializer(_boos, many=True).data
        _boos = {b['id']:b for b in _boos}
        return json.dumps(_boos)

    @property
    def serialized(self):
        # _user = UserSerializer([self], many=True).data[0]
        _user = UserSerializer(self).data
        # _user['boos'] = {boo['id']:boo for boo in _user['boos']}
        return json.dumps(_user)

    def set_boo(self, boo_id):
        self.boo_selected = boo_id
        self.save()

    def delete_boo(self):
        self.boo.delete()
        boos_id = Boo.objects.filter(user=self).values_list('id', flat=True)
        self.set_boo(max(boos_id))
        #print(boos_id, max(boos_id))

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            boo = Boo.objects.create(user=self)
            self.boo_selected = boo.id
            super().save(*args, **kwargs)


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
        return self.type + ' | ' + self.category + ' | ' + str(self.id)



class Mask(BigIdAbstract):
    masked = models.BooleanField(default=False, null=False, blank=False)
    top = models.FloatField(default=0, null=False, blank=False)
    left = models.FloatField(default=0, null=False, blank=False)
    width = models.FloatField(default=100, null=False, blank=False)
    # height = models.FloatField(default=15, null=False, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        fmt = '{maskbase} | T={top}, L={left}, W={width}, H={height}'
        return fmt.format(maskbase=self.maskbase, top=self.top, left=self.left, width=self.width, height=self.height)


class EyeMask(Mask):
    maskbase = models.ForeignKey(MaskBase, null=False, blank=False, on_delete=models.CASCADE, default=1)
    height = models.FloatField(default=15, null=False, blank=False)


class MouthMask(Mask):
    maskbase = models.ForeignKey(MaskBase, null=False, blank=False, on_delete=models.CASCADE, default=35)
    height = models.FloatField(default=30, null=False, blank=False)


def _characterpix_path(instance, fname):
    fname = str(datetime.now()) + fname
    fmt = 'character/{category}/{fname}'
    return fmt.format(fname=fname, category=instance.category)


class Character(BigIdAbstract):
    category = models.CharField(max_length=50, null=False, blank=False, default='base')
    pix = models.ImageField(upload_to=_characterpix_path, max_length=500, null=False, blank=False)

    def __str__(self):
        return self.category + ' | ' + str(self.id)



def _profilepix_path(instance, fname):
    try:
        user = instance.boo.user.email
    except:
        user = 'anonymous'

    fname = str(datetime.now()) + '__' + fname
    fmt = 'user/{user}/{fname}'
    return fmt.format(user=user, fname=fname)


class Profile(BigIdAbstract):
    PROFILE_TYPES = ( ('CHARACTER', 'character'), ('IMAGE', 'image'), ('TEXT', 'text') )
    type = models.CharField(max_length=10, choices=PROFILE_TYPES, default='CHARACTER', null=False, blank=False)
    pix = models.ImageField(upload_to=_profilepix_path, max_length=500, null=True, blank=True)
    character = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=_profilepix_path, max_length=500, null=True, blank=True)
    text = models.CharField(max_length=10, null=True, blank=True)
    eyemask = models.OneToOneField(EyeMask, null=True, blank=True, on_delete=models.SET_NULL)
    mouthmask = models.OneToOneField(MouthMask, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type + ' | ' + str(self.id) #os.path.basename(self.pix.name)

    def save(self, *args, **kwargs):
        if self.character is None:
            self.character = Character.objects.get(pk=1)

        if self.eyemask is None:
            self.eyemask = EyeMask.objects.create()

        if self.mouthmask is None:
            self.mouthmask = MouthMask.objects.create()

        if not self.pix:
            self.pix = 'material/character_default.png'
            # self.pix = 'material/SIDEB_CHARACTER_M_01.png'

        # if not self.image:
        #     self.image = 'material/character_default.png'

        super().save(*args, **kwargs)


    @property
    def serialized(self):
        _profile = ProfileSerializer([self], many=True).data[0]
        return json.dumps(_profile)


class Boo(BigIdAbstract, ModelWithFlag):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=200, blank=True, null=True)
    profile = models.OneToOneField(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.IntegerField(default=0)

    styletags = models.ManyToManyField(Styletag, blank=True)
    fashiontems = models.ManyToManyField(Fashiontem, blank=True)

    nposts = models.IntegerField(default=0)
    nfollowers = models.IntegerField(default=0)

    def __str__(self):
        return self.nick + ' | ' + self.user.email

    @property
    def selected(self):
        return self.user.boo_selected == self.id

    def save(self, *args, **kwargs):
        if (self.nick is None) or (self.nick.strip() == ''):
            self.nick = self.user.email.split('@')[0]

        if self.profile is None:
            self.profile  = Profile.objects.create()

        # 포스트가 새로 만들어지거나 팔로우할때 아래 코드가 실행되게 하고 싶은데
        # 늘 두개씩 다 실행시키는게 불필요해보이기도 하고
        # 팔로우 한후에 Boo가 자동저장되는지도 불확실
        self.nposts = self.post_set.count()
        self.nfollowers = self.get_flags(status=FOLLOW).count()

        super().save(*args, **kwargs)

    @property
    def serialized(self):
        # _boo = BooSerializer([self], many=True).data[0]
        _boo = BooSerializer(self).data
        return json.dumps(_boo)

    def follow(self, boo_id, note=None):
        boo = Boo.objects.get(pk=boo_id)
        boo.set_flag(self, note=note, status=FOLLOW)
        boo.save()

    def unfollow(self, boo_id):
        boo = Boo.objects.get(pk=boo_id)
        boo.remove_flag(self, status=FOLLOW)
        boo.save()

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

    @property
    def followees(self):
        return Boo.objects.filter(id__in=self.followees_id)

    # @property
    # def network(self):
    #     _network = {
    #         'followers': SimplebooSerializer(self.followers, many=True).data,
    #         'followees': SimplebooSerializer(self.followees, many=True).data
    #     }
    #     return json.dumps(_network)

    @property
    def voting_record(self):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return {f.object_id:f.status for f in Flager.objects.filter(q, user=self)}

    # @property
    def iposts(self, type):
        if type=='own':
            return list(self.post_set.values_list('id', flat=True))

        elif type=='follow':
            return list(Post.objects.filter(boo_id__in=self.followees_id).values_list('id', flat=True))

        elif type=='attend':
            q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
            return list(Flager.objects.filter(q, user=self).values_list('object_id', flat=True))


    @property
    def ilikes_comment(self):
        return list(Flager.objects.filter(status=LIKE_COMMENT, user=self).values_list('object_id', flat=True))

    # @property
    # def nfollowers(self):
    #     return self.get_flags(status=FOLLOW).count()
    #
    # @property
    # def nfollowees(self):
    #     return Flager.objects.filter(status=FOLLOW, user=self).count()

    # @property
    # def nposts(self):
    #     return Post.objects.filter(boo=self).count()



class Post(BigIdAbstract, ModelWithFlag):
    boo = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_DEFAULT, default=BOO_DELETED)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()

    nvotes_up = models.IntegerField(default=0)
    nvotes_down = models.IntegerField(default=0)

    def __str__(self):
        return str(self.created_at) + ((' | ' + str(self.boo)) if self.boo else '')

    def save(self, *args, **kwargs):
        # 아래 두줄의 순서가 중요할까?
        super().save(*args, **kwargs)
        self.boo.save()

    @property
    def type(self):
        return self.__class__.__name__.lower()

    '''
    child로 downcast
    '''
    @property
    def cast(self):
        for subclass in self.__class__.__subclasses__():
            try:
                return getattr(self, subclass.__name__.lower())
            except:
                pass

        return self


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

        self.nvotes_up = self._nvotes_up
        self.nvotes_down = self._nvotes_down
        self.save()


    @property
    def ivoters(self):
        _ivoters = {f.user.id:f.status for f in Flager.objects.filter(object_id=self.id)}
        return _ivoters


    @property
    def _nvotes_up(self):
        return Flager.objects.filter(status=VOTE_UP, object_id=self.id).count()

    @property
    def _nvotes_down(self):
        return Flager.objects.filter(status=VOTE_DOWN, object_id=self.id).count()


    @property
    def ncomments(self):
        return self.comment_set.filter(boo__isnull=False).count()

    @property
    def popularity(self):
        return self.nvotes_up + self.nvotes_down + self.ncomments


def _postpix_path(instance, fname):
    try:
        user = instance.boo.user.email
    except:
        user = 'anonymous'

    now = datetime.now()
    fname = str(now) + '__' + fname
    fmt = 'post/{year}/{month}/{day}/{user}/{fname}'
    return fmt.format(year=now.year, month=now.month, day=now.day, user=user, fname=fname)


class PostVoteOX(Post):
    OX_KEYS = ( ('OX', 'OX'), ('SM', '살말') )
    keys = models.CharField(max_length=2, choices=OX_KEYS, default='OX', null=False, blank=False)
    pix = models.ImageField(upload_to=_postpix_path, max_length=500, null=False, blank=False)

    def __str__(self):
        return 'OX | ' + super().__str__()


class PostVoteAB(Post):
    pix_a = models.ImageField(upload_to=_postpix_path, max_length=500, null=False, blank=False)
    pix_b = models.ImageField(upload_to=_postpix_path, max_length=500, null=False, blank=False)

    pixlabel_a = models.TextField(max_length=200, blank=True, null=True)
    pixlabel_b = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return 'AB | ' + super().__str__()


class Comment(BigIdAbstract, ModelWithFlag):
    boo = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def like(self, boo, note=None):
        # boo = Boo.objects.get(pk=boo_id)
        self.set_flag(boo, note=note, status=LIKE_COMMENT)

    def delike(self, boo):
        # boo = Boo.objects.get(pk=boo_id)
        self.remove_flag(boo, status=LIKE_COMMENT)

    def __str__(self):
        return str(self.created_at) + ' | ' +  self.text + ((' | ' + str(self.boo)) if self.boo else '')


class EyeMaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeMask
        fields = ['id', 'maskbase', 'masked', 'top', 'left', 'width', 'height']
        read_only_fields = ['id']


class MouthMaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouthMask
        fields = ['id', 'maskbase', 'masked', 'top', 'left', 'width', 'height']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    eyemask = EyeMaskSerializer(required=False)
    mouthmask = MouthMaskSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'type', 'pix', 'character', 'image', 'text', 'eyemask', 'mouthmask']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # initial_data에서 가져오는게 핵심이다
        # 만약 eyemask를 validated_data에서 가져온다면,
        # 이미 serializer로 가공된 data(예.maskbase id가 아니라 maskbase 객체로 가공)가 넘어간다
        eyemask_data = self.initial_data.pop('eyemask', None)
        mouthmask_data = self.initial_data.pop('mouthmask', None)

        instance.type = validated_data.get('type', instance.type)
        instance.pix = validated_data.get('pix', instance.pix)
        instance.character = validated_data.get('character', instance.character)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        if eyemask_data:
            ser = EyeMaskSerializer(instance.eyemask, data=eyemask_data, partial=True)
            if ser.is_valid():
                ser.save()
            else:
                print('something wrong when updating eyemask data')

        if mouthmask_data:
            ser = MouthMaskSerializer(instance.mouthmask, data=mouthmask_data, partial=True)
            if ser.is_valid():
                ser.save()
            else:
                print('something wrong when updating mouthmask data')

        return instance


# class StyletagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Styletag
#         fields = ['id', 'tag']


# https://stackoverflow.com/questions/39104575/django-rest-framework-recursive-nested-parent-serialization
class BasebooSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    styletags = serializers.SerializerMethodField()
    fashiontems = serializers.SerializerMethodField()
    # styletags = StyletagSerializer(read_only=True, many=True)

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'nfollowers', 'nposts', 'styletags', 'fashiontems']
        read_only_fields = fields

    def get_profile(self, obj):
        return {'pix': obj.profile.pix.url}

    def get_styletags(self, obj):
        return list(obj.styletags.values_list('id', flat=True))

    def get_fashiontems(self, obj):
        return list(obj.fashiontems.values_list('id', flat=True))

# class BasebooSerializer(serializers.ModelSerializer):
#     profile = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Boo
#         fields = ['id', 'nick', 'text', 'profile', 'nfollowers', 'nposts', 'posts']
#         read_only_fields = fields
#
#     def get_profile(self, obj):
#         return {'pix': obj.profile.pix.url}



class BooSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    styletags = serializers.SerializerMethodField()
    fashiontems = serializers.SerializerMethodField()

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'key', 'followees_id', 'nfollowers', 'voting_record', 'ilikes_comment', 'nposts', 'styletags', 'fashiontems']
        read_only_fields = ['id', 'followers_id', 'followees_id', 'voting_record', 'ilikes_comment', 'nposts']

    def get_styletags(self, obj):
        return list(obj.styletags.values_list('id', flat=True))

    def get_fashiontems(self, obj):
        return list(obj.fashiontems.values_list('id', flat=True))

    def update(self, instance, validated_data):
        profile_data = self.initial_data.pop('profile', None)

        instance.user = validated_data.get('user', instance.user)
        instance.nick = validated_data.get('nick', instance.nick)
        instance.text = validated_data.get('text', instance.text)
        instance.key = validated_data.get('key', instance.key)
        instance.save()

        if profile_data:
            ser = ProfileSerializer(instance.profile, data=profile_data, partial=True)
            if ser.is_valid():
                ser.save()
            else:
                print('something wrong when updating profile data')

        return instance


class UserSerializer(serializers.ModelSerializer):
    boo = BooSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'boo_selected', 'boo']
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'boo', 'text', 'created_at']
        read_only_fields = ['id']



class BoopostVoteOXSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVoteOX
        fields = ['id', 'text', 'pix', 'keys', 'nvotes_up', 'nvotes_down', 'ncomments']
        read_only_fields = fields


class BoopostVoteABSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVoteAB
        fields = ['id', 'text', 'pix_a', 'pix_b', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down', 'ncomments']
        read_only_fields = fields


class BoopostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        if isinstance(instance, PostVoteOX):
            return {'type':'postvoteox', **BoopostVoteOXSerializer(instance=instance).data}

        elif isinstance(instance, PostVoteAB):
            return {'type':'postvoteab', **BoopostVoteABSerializer(instance=instance).data}


class PostVoteOXSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()

    class Meta:
        model = PostVoteOX
        fields = ['id', 'boo', 'text', 'pix', 'keys', 'nvotes_up', 'nvotes_down', 'ncomments']#, 'ivoters']
        read_only_fields = ['id', 'nvotes_up', 'nvotes_down']


class PostVoteABSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()

    class Meta:
        model = PostVoteAB
        fields = ['id', 'boo', 'text', 'pix_a', 'pix_b', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down', 'ncomments']#, 'ivoters']
        read_only_fields = ['id', 'nvotes_up', 'nvotes_down']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        if isinstance(instance, PostVoteOX):
            return {'type':'postvoteox', **PostVoteOXSerializer(instance=instance).data}

        elif isinstance(instance, PostVoteAB):
            return {'type':'postvoteab', **PostVoteABSerializer(instance=instance).data}

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # serializer queryset 최적화하기
        # http://ses4j.github.io/2015/11/23/optimizing-slow-django-rest-framework-performance/
        queryset = queryset.select_related('boo', 'boo__profile')
        queryset = queryset.prefetch_related('comment_set')
        return queryset

    # 이부분은 안쓰게 되는거 같다. pix를 어떻게 serializer로 저장하는지 모르겠다
    # def create(self, validated_data):
    #     _type = self.initial_data.pop('type')
    #
    #     if _type == 'postvoteox':
    #         ser = PostVoteOXSerializer(data=self.initial_data, partial=True)
    #
    #     elif _type == 'postvoteab':
    #         ser = PostVoteABSerializer(data=self.initial_data, partial=True)
    #
    #     if ser.is_valid():
    #         return ser.save()
    #
    #     else:
    #         print('something wrong when creating post data')
    #         return None
    #
    #
    # def update(self, instance, validated_data):
    #     _type = instance.__class__.__name__.lower()
    #
    #     if _type == 'postvoteox':
    #         ser = PostVoteOXSerializer(instance, data=self.initial_data, partial=True)
    #
    #     elif _type == 'postvoteab':
    #         ser = PostVoteABSerializer(instance, data=self.initial_data, partial=True)
    #
    #     if ser.is_valid():
    #         ser.save()
    #
    #     else:
    #         print('something wrong when updating post data')
    #
    #     return instance
