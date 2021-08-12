from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
# from vote.models import VoteModel
from siteflags.models import ModelWithFlag, FlagBase
from datetime import datetime, date, timedelta
from django.conf import settings
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.db.models import F, Q, Sum, Count, Case, When
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.functional import classproperty
from django.contrib.contenttypes.models import ContentType
# from notifications.base.models import AbstractNotification
from notifications.signals import notify

from IPython.core.debugger import set_trace
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
import json
import os
import re
import collections
import random

# from gensim.models import Doc2Vec


VOTE_UP = 0
VOTE_DOWN = 1
FOLLOW = 10
LIKE_COMMENT = 100

BOO_DELETED = 97
GUESTBOO = 363

# model_path = os.path.join(settings.BASE_DIR, 'data', 'doc2vec.model')
# d2v = Doc2Vec.load(model_path)


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


# class Notification(AbstractNotification):
#     class Meta(AbstractNotification.Meta):
#         abstract = False


class Flager(FlagBase):
    user = models.ForeignKey('Boo', related_name='%(class)s_users', verbose_name='Boo', on_delete=models.CASCADE)

    class Meta(FlagBase.Meta):
        # note까지 같아야 같은 걸로 취급.
        # guest 사용자들이 하나의 부캐로 여러번 보팅할수 있도록
        # 2021.02.16
        unique_together = (
            'content_type',
            'object_id',
            'user',
            'status',
            'note'
        )

    @classmethod
    def vote_on(cls, obj, boo, status, note):
        try:
            cls.objects.create(linked_object=obj, user=boo, status=status, note=note)
        except:
            pass

    @classmethod
    def vote_off(cls, obj, boo, status, note):
        ctype = ContentType.objects.get_for_model(obj)

        try:
            cls.objects.get(content_type=ctype, object_id=obj.id, user=boo, status=status, note=note).delete()
        except:
            pass

    @classmethod
    def vote_up(cls, obj, boo, note):
        cls.vote_on(obj, boo, VOTE_UP, note)
        cls.vote_off(obj, boo, VOTE_DOWN, note)

    @classmethod
    def vote_down(cls, obj, boo, note):
        cls.vote_off(obj, boo, VOTE_UP, note)
        cls.vote_on(obj, boo, VOTE_DOWN, note)

    @classmethod
    def vote_clear(cls, obj, boo, note):
        cls.vote_off(obj, boo, VOTE_UP, note)
        cls.vote_off(obj, boo, VOTE_DOWN, note)

    @classmethod
    def like_comment(cls, obj, boo, note):
        try:
            cls.objects.create(linked_object=obj, user=boo, status=LIKE_COMMENT, note=note)
        except:
            pass

    @classmethod
    def delike_comment(cls, obj, boo, note):
        ctype = ContentType.objects.get_for_model(obj)

        try:
            cls.objects.get(content_type=ctype, object_id=obj.id, user=boo, status=LIKE_COMMENT, note=note).delete()
        except:
            pass


class Label(BigIdAbstract):
    label = models.CharField(max_length=20, null=False, blank=False)
    key = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

class Genderlabel(Label):
    pass

class Agelabel(Label):
    pass

class Bodylabel(Label):
    pass

class Stylelabel(Label):
    pass

class Itemlabel(Label):
    pass


class User(AbstractEmailUser):
    boo_selected = models.IntegerField(default=0)

    @classmethod
    def guest(cls):
        return cls.objects.get(email=GUEST)

    @property
    def has_active_boo(self):
        return self.boo_set.filter(active=True).count() > 0

    @property
    def boo(self):
        return self.boo_set.get(pk=self.boo_selected)
        # try:
        #     return self.boo_set.get(pk=self.boo_selected)
        #
        # except:
        #     active_boos = self.boo_set.filter(active=True)
        #
        #     if active_boos.count() > 0:
        #         self.set_boo(max(active_boos.values_list('id', flat=True)))
        #
        #     else:
        #         boo = Boo.objects.create(user=self)
        #         self.set_boo(boo.id)
        #
        #     return self.boo_set.get(pk=self.boo_selected)


    @property
    def other_boos(self):
        _boos = self.boo_set.filter(active=True).exclude(pk=self.boo_selected)
        _boos = BooSerializer(_boos, many=True).data
        _boos = {b['id']:b for b in _boos}
        return json.dumps(_boos)

    @property
    def serialized(self):
        _user = UserSerializer(self).data
        return json.dumps(_user)

    def create_default_boo(self):
        boo = Boo.objects.create(user=self)
        self.set_boo(boo.id)

    def set_boo(self, boo_id):
        self.boo_selected = boo_id
        self.save()

    def delete_boo(self):
        # self.boo.delete()
        boo = self.boo
        boo.active = False
        boo.save()
        boos_id = self.boo_set.filter(active=True).values_list('id', flat=True)
        # boos_id = Boo.objects.filter(user=self, active=True).values_list('id', flat=True)
        self.set_boo(max(boos_id))


# class Session(BigIdAbstract):
#     sessionkey = models.CharField(max_length=200, blank=False, null=False)
#     user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
#     checkin = models.DateTimeField(auto_now_add=True)
#     checkout = models.DateTimeField(default=timezone.now, null=False)
#
#     # https://stackoverflow.com/questions/42239818/how-to-set-the-default-of-a-jsonfield-to-empty-list-in-django-and-django-jsonfie
#     view = models.JSONField(null=True, default=list)
#
#     def __str__(self):
#         return self.sessionkey + ' | ' + str(self.checkin)
#
#     @classmethod
#     def call(cls, request):
#         try:
#             session = cls.objects.get(sessionkey=request.session.session_key)
#             # session.checkout = datetime.now()
#             # session.save()
#
#         except:
#             request.session.create()
#             session = cls.objects.create(sessionkey=request.session.session_key)
#
#         # if request.user.is_authenticated:
#         #     session.user = request.user
#         #     session.save()
#         #
#         # else:
#         #     session.user = None
#         #     session.save()
#
#         return session
#
#
#     # @property
#     # def guest(self):
#     #     return {
#     #         'sessionkey': self.sessionkey,
#     #         'view': self.view
#     #     }
#
#     def vote(self, post_id, action):
#         _post = Post.objects.get(pk=post_id)
#
#         if self.user:
#             _post.vote(int(action), self.user.boo)
#
#         else:
#             _post.vote(int(action), Boo.guestboo, note=self.sessionkey)
#
#     @property
#     def fit(self):
#         return []


def _profilepix_path(instance, fname):
    try:
        user = instance.boo.user.email
    except:
        user = 'anonymous'

    fname = str(datetime.now()) + '__' + fname
    fmt = 'user/{user}/{fname}'
    return fmt.format(user=user, fname=fname)


class Profile(BigIdAbstract):
    pix = models.ImageField(upload_to=_profilepix_path, max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pix:
            self.pix = 'material/ghost_' + random.choice(['b','m','p','y']) + '.png'
            # self.pix = 'material/character_default.png'

        super().save(*args, **kwargs)


class Link(BigIdAbstract):
    url = models.URLField(max_length=200, blank=False, null=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    # public = models.BooleanField(default=True)

    def __str__(self):
        return self.url


class Boo(BigIdAbstract, ModelWithFlag):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=200, blank=True, null=True)
    profile = models.OneToOneField(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    genderlabels = models.ManyToManyField(Genderlabel, blank=True)
    agelabels = models.ManyToManyField(Agelabel, blank=True)
    bodylabels = models.ManyToManyField(Bodylabel, blank=True)
    stylelabels = models.ManyToManyField(Stylelabel, blank=True)
    itemlabels = models.ManyToManyField(Itemlabel, blank=True)

    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)

    links = models.ManyToManyField(Link, blank=True)


    def __str__(self):
        return self.nick + ' | ' + self.user.email

    # @property
    # def links_list(self):
    #     return []
        # if self.links:
        #     _links = self.links.split(',')
        #     return [int(i) for i in _links]
        #
        # else:
        #     return []

    @classproperty
    def guestboo(cls):
        return cls.objects.get(id=GUESTBOO)

    @classmethod
    def guestboo_serialized(cls, sessionkey):
        _guestboo = GuestbooSerializer(cls.guestboo, context={'sessionkey':sessionkey}).data
        return json.dumps(_guestboo)

    @property
    def is_guestboo(self):
        return self.id == GUESTBOO

    @property
    def selected(self):
        return self.user.boo_selected == self.id

    def save(self, *args, **kwargs):
        if (self.nick is None) or (self.nick.strip() == ''):
            # self.nick = ''
            self.nick = self.user.email.split('@')[0]

        if self.profile is None:
            self.profile  = Profile.objects.create()

        # 포스트가 새로 만들어지거나 팔로우할때 아래 코드가 실행되게 하고 싶은데
        # 늘 두개씩 다 실행시키는게 불필요해보이기도 하고
        # 팔로우 한후에 Boo가 자동저장되는지도 불확실
        # self.nposts = self.post_set.count()
        # self.nfollowers = self.get_flags(status=FOLLOW).count()

        super().save(*args, **kwargs)

    @property
    def nfollowers(self):
        return self.get_flags(status=FOLLOW).count()

    @property
    def nfollowees(self):
        return Flager.objects.filter(status=FOLLOW, user=self).count()

    @property
    def nposts(self):
        return self.post_set.count()

    @property
    def ncomments(self):
        return self.comment_set.count()

    @property
    def nlikes_comment(self):
        return Flager.objects.filter(status=LIKE_COMMENT, user=self).count()

    @property
    def nvotes(self):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return Flager.objects.filter(q, user=self).count()

    @property
    def serialized(self):
        # _boo = BooSerializer([self], many=True).data[0]
        _boo = BooSerializer(self).data
        return json.dumps(_boo)

    def follow(self, boo_id, note=None):
        boo = Boo.objects.get(pk=boo_id)
        boo.set_flag(self, note=note, status=FOLLOW)
        # notify.send(self, recipient=boo.user, verb='follow')
        boo.save()

    def unfollow(self, boo_id):
        boo = Boo.objects.get(pk=boo_id)
        boo.remove_flag(self, status=FOLLOW)
        # notify.send(self, recipient=boo.user, verb='unfollow')
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

    @property
    def voting_record(self):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return {f.object_id:f.status for f in Flager.objects.filter(q, user=self)}

    def iposts(self, type):
        # if (self.user.id == hidden_user) and (self.nick == hidden_boo_nick):
        if self.hidden:
            return []

        elif type=='own':
            return list(self.post_set.order_by('-id').values_list('id', flat=True))

        elif type=='follow':
            return list(Post.objects.order_by('-id').filter(boo_id__in=self.followees_id).values_list('id', flat=True))

        elif type=='attend':
            q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
            return list(Flager.objects.order_by('-id').filter(q, user=self).values_list('object_id', flat=True))


    @property
    def ilikes_comment(self):
        return list(Flager.objects.filter(status=LIKE_COMMENT, user=self).values_list('object_id', flat=True))


    # @property
    # def baseid(self):
    #     styletags = list(self.styletags.values_list('tag', flat=True))
    #     fashiontems = list(self.fashiontems.values_list('item', flat=True))
    #     nick = self.nick.lower()
    #     text = self.text.lower() if self.text else ''
    #     return preproc(nick + ' ' + text).split(' ') + styletags + fashiontems
    #
    # @property
    # def votokens(self):
    #     pos = []
    #     neg = []
    #
    #     votes = self.voting_record
    #     for pix in Postpix.objects.filter(post_id__in=votes).select_related('post'):
    #         act = votes[pix.post.id]
    #         desc = preproc(pix.desc.lower()).split(' ') if pix.desc else []
    #
    #         if pix.key=='ox' and act==0:
    #             pos += pix.tokens.split(', ') + desc
    #
    #         elif pix.key=='ox' and act==1:
    #             neg += pix.tokens.split(', ') + desc
    #
    #         elif (pix.key=='a' and act==0) or (pix.key=='b' and act==1):
    #             pos += pix.tokens.split(', ') + desc
    #
    #         elif (pix.key=='a' and act==1) or (pix.key=='b' and act==0):
    #             neg += pix.tokens.split(', ') + desc
    #
    #     return { 'pos_tokens': pos, 'neg_tokens': neg }

    @property
    def fit(self):
        return []
        # try:
        #     votokens = self.votokens
        #     pos_tokens = votokens['pos_tokens']
        #     neg_tokens = votokens['neg_tokens']
        #     pos_freq = collections.Counter(pos_tokens)
        #     neg_freq = collections.Counter(neg_tokens)
        #
        #     like_tokens = list(dict((pos_freq - neg_freq).most_common(10)).keys())
        #     dislike_tokens = list(dict((neg_freq - pos_freq).most_common(10)).keys())
        #
        #     pos_vec = d2v.infer_vector(pos_tokens, epochs=500)
        #     neg_vec = d2v.infer_vector(neg_tokens, epochs=500)
        #     baseid_vec = d2v.infer_vector(self.baseid, epochs=500)
        #     brand_freq = d2v.docvecs.most_similar(positive=[pos_vec, baseid_vec], negative=[neg_vec], topn=5)
        #     yourbrands = list(dict(brand_freq).keys())
        #
        # except:
        #     like_tokens = []
        #     dislike_tokens = []
        #     baseid_vec = d2v.infer_vector(self.baseid, epochs=500)
        #     brand_freq = d2v.docvecs.most_similar(positive=[baseid_vec], topn=5)
        #     yourbrands = list(dict(brand_freq).keys())
        #
        # return {'likes':like_tokens, 'dislikes':dislike_tokens, 'yourbrands':yourbrands}



class Post(BigIdAbstract, ModelWithFlag):
    boo = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_DEFAULT, default=BOO_DELETED)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()

    # nvotes_up = models.IntegerField(default=0)
    # nvotes_down = models.IntegerField(default=0)

    def __str__(self):
        return str(self.created_at) + ((' | ' + str(self.boo)) if self.boo else '')

    def save(self, *args, **kwargs):
        # 아래 두줄의 순서가 중요할까?
        super().save(*args, **kwargs)
        self.boo.save()

    @classmethod
    def iposts(cls, type):
        excl = Q(boo_id=BOO_DELETED) | Q(boo__hidden=True)

        if type == 'history':
            return Post.objects.exclude(excl).order_by('-created_at').values_list('id', flat=True)

        elif type == 'hot':
            q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
            ago_2w = datetime.now() - timedelta(days=7)
            return Flager.objects.filter(q, time_created__gte=ago_2w).values('object_id').annotate(nvotes=Count('object_id')).order_by('-nvotes').values_list('object_id', flat=True)
            # return Post.objects.exclude(excl).annotate(ordering=F('nvotes_up') + F('nvotes_down')).order_by('-ordering').values_list('id', flat=True)

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


    # def vote(self, action, boo=None):
    def vote(self, action, boo, note=''):
        # up
        if action==VOTE_UP:
            Flager.vote_up(self, boo, note)

        # down
        elif action==VOTE_DOWN:
            Flager.vote_down(self, boo, note)

        # clear
        else:
            Flager.vote_clear(self, boo, note)

        # self.nvotes_up = self._nvotes_up
        # self.nvotes_down = self._nvotes_down
        # self.save()


    @property
    def ivoters(self):
        _ivoters = {f.user.id:f.status for f in Flager.objects.filter(object_id=self.id)}
        return _ivoters


    @property
    def nvotes_up(self):
        return Flager.objects.filter(status=VOTE_UP, object_id=self.id).count()

    @property
    def nvotes_down(self):
        return Flager.objects.filter(status=VOTE_DOWN, object_id=self.id).count()


    @property
    def ncomments(self):
        return self.comment_set.filter(boo__isnull=False).count()


def _postpix_path(instance, fname):
    try:
        user = instance.boo.user.email
    except:
        user = 'anonymous'

    now = datetime.now()
    fname = str(now) + '__' + fname
    fmt = 'post/{year}/{month}/{day}/{user}/{fname}'
    return fmt.format(year=now.year, month=now.month, day=now.day, user=user, fname=fname)

def _postpix_path2(instance, fname):
    try:
        user = instance.post.boo.user.email
    except:
        user = 'anonymous'

    now = datetime.now()
    fname = str(now) + '__' + fname
    fmt = 'post/{year}/{month}/{day}/{user}/{fname}'
    return fmt.format(year=now.year, month=now.month, day=now.day, user=user, fname=fname)

def _commentpix_path(instance, fname):
    try:
        user = instance.comment.boo.user.email
    except:
        user = 'anonymous'

    now = datetime.now()
    fname = str(now) + '__' + fname
    fmt = 'comment/{year}/{month}/{day}/{user}/{fname}'
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


class PostQA(Post):
    pix = models.ImageField(upload_to=_postpix_path, max_length=500, null=False, blank=False)

    def __str__(self):
        return 'QA | ' + super().__str__()


class Comment(BigIdAbstract, ModelWithFlag):
    boo = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=500, blank=False, null=False)
    mention = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL, related_name='mentioned_comment_set')
    created_at = models.DateTimeField(auto_now_add=True)

    def like(self, boo, note=''):
        Flager.like_comment(self, boo, note)
        # self.set_flag(boo, note=note, status=LIKE_COMMENT)

    def delike(self, boo, note=''):
        Flager.delike_comment(self, boo, note)
        # self.remove_flag(boo, status=LIKE_COMMENT)

    def __str__(self):
        return str(self.created_at) + ' | ' +  self.text + ((' | ' + str(self.boo)) if self.boo else '')


class Commentpix(BigIdAbstract):
    comment = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.SET_NULL)
    img = models.ImageField(upload_to=_commentpix_path, max_length=500, null=False, blank=False)


class Postpix(BigIdAbstract):
    key = models.CharField(max_length=5, default='ox', null=False, blank=False)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    img = models.ImageField(upload_to=_postpix_path2, max_length=500, null=False, blank=False)
    desc = models.TextField(max_length=200, blank=True, null=True)
    tokens = models.TextField(max_length=500, blank=True, null=True)

    @property
    def owner(self):
        return self.post.boo.nick if self.post is not None else None


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'pix']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # initial_data에서 가져오는게 핵심이다
        # 만약 eyemask를 validated_data에서 가져온다면,
        # 이미 serializer로 가공된 data(예.maskbase id가 아니라 maskbase 객체로 가공)가 넘어간다
        # eyemask_data = self.initial_data.pop('eyemask', None)
        # mouthmask_data = self.initial_data.pop('mouthmask', None)

        # instance.type = validated_data.get('type', instance.type)
        instance.pix = validated_data.get('pix', instance.pix)
        # instance.character = validated_data.get('character', instance.character)
        # instance.image = validated_data.get('image', instance.image)
        # instance.text = validated_data.get('text', instance.text)
        instance.save()

        # if eyemask_data:
        #     ser = EyeMaskSerializer(instance.eyemask, data=eyemask_data, partial=True)
        #     if ser.is_valid():
        #         ser.save()
        #     else:
        #         print('something wrong when updating eyemask data')
        #
        # if mouthmask_data:
        #     ser = MouthMaskSerializer(instance.mouthmask, data=mouthmask_data, partial=True)
        #     if ser.is_valid():
        #         ser.save()
        #     else:
        #         print('something wrong when updating mouthmask data')

        return instance



class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'url']
        read_only_fields = fields


# https://stackoverflow.com/questions/39104575/django-rest-framework-recursive-nested-parent-serialization
class BasebooSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'active', 'nfollowers', 'nposts', 'genderlabels', 'agelabels', 'bodylabels', 'stylelabels', 'itemlabels', 'links']
        read_only_fields = fields

    def get_profile(self, obj):
        return {'pix': obj.profile.pix.url}

    def get_links(self, obj):
        return list(obj.links.filter(user_id=obj.user.id).values_list('url', flat=True))
        # return list(obj.user.link_set.filter(id__in=obj.links_list).values_list('url', flat=True))


class GuestbooSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    voting_record = serializers.SerializerMethodField()
    ilikes_comment = serializers.SerializerMethodField()

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'voting_record', 'ilikes_comment']
        read_only_fields = fields

    def get_profile(self, obj):
        return {'pix': obj.profile.pix.url}

    def get_voting_record(self, obj):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return {f.object_id:f.status for f in Flager.objects.filter(q, user=obj, note=self.context.get('sessionkey'))}

    def get_ilikes_comment(self, obj):
        return list(Flager.objects.filter(status=LIKE_COMMENT, user=obj, note=self.context.get('sessionkey')).values_list('object_id', flat=True))


class BooSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    # links = serializers.SerializerMethodField()
    # links = LinkSerializer(source='link_set', required=False, many=True)

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'active', 'followees_id', 'nfollowers', 'voting_record', 'ilikes_comment', 'nposts', 'fit', 'genderlabels', 'agelabels', 'bodylabels', 'stylelabels', 'itemlabels', 'links']
        read_only_fields = ['id', 'active', 'followees_id', 'voting_record', 'ilikes_comment', 'nposts', 'fit', 'links']

    # def get_links(self, obj):
    #     return obj.links_list
        # if obj.links:
        #     ilinks = obj.links.split(',')
        #     return [int(i) for i in ilinks]
        # else:
        #     return []

    def update(self, instance, validated_data):
        profile_data = self.initial_data.pop('profile', None)

        instance.user = validated_data.get('user', instance.user)
        instance.nick = validated_data.get('nick', instance.nick)
        instance.text = validated_data.get('text', instance.text)
        # instance.key = validated_data.get('key', instance.key)
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
    links = LinkSerializer(source='link_set', required=False, many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'boo_selected', 'boo', 'links']
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()
    mention = serializers.SerializerMethodField()
    attached = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'boo', 'text', 'mention', 'attached', 'created_at']
        read_only_fields = ['id']

    def get_mention(self, obj):
        if obj.mention:
            return {'id': obj.mention.id, 'nick': obj.mention.nick}

    def get_attached(self, obj):
        try:
            # print(obj.commentpix_set.all())
            # print(list(ob.commentpix_set.all())[0])
            return { 'img': obj.commentpix_set.first().img.url }
            # return obj.commentpix_set.values('img')[0]
        except:
            pass
        # if commentpixes.count() > 0:
        #     return commentpixes[0]


# class BoopostVoteOXSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostVoteOX
#         fields = ['id', 'text', 'pix', 'keys', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at']
#         read_only_fields = fields
#
#
#
# class BoopostVoteABSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostVoteAB
#         fields = ['id', 'text', 'pix_a', 'pix_b', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at']
#         read_only_fields = fields
#
#
# class BoopostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         if isinstance(instance, PostVoteOX):
#             return {'type':'postvoteox', **BoopostVoteOXSerializer(instance=instance).data}
#
#         elif isinstance(instance, PostVoteAB):
#             return {'type':'postvoteab', **BoopostVoteABSerializer(instance=instance).data}


class PostVoteOXSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()
    # nvotes_up = serializers.SerializerMethodField()
    # nvotes_down = serializers.SerializerMethodField()

    class Meta:
        model = PostVoteOX
        fields = ['id', 'boo', 'text', 'pix', 'keys', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at']
        read_only_fields = ['id', 'nvotes_up', 'nvotes_down']

    # def get_nvotes_up(self, obj):
    #     return obj._nvotes_up
    #
    # def get_nvotes_down(self, obj):
    #     return obj._nvotes_down


class PostVoteABSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()
    # nvotes_up = serializers.SerializerMethodField()
    # nvotes_down = serializers.SerializerMethodField()

    class Meta:
        model = PostVoteAB
        fields = ['id', 'boo', 'text', 'pix_a', 'pix_b', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at']
        read_only_fields = ['id', 'nvotes_up', 'nvotes_down']

    # def get_nvotes_up(self, obj):
    #     return obj._nvotes_up
    #
    # def get_nvotes_down(self, obj):
    #     return obj._nvotes_down


class PostQASerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()
    # nvotes_up = serializers.SerializerMethodField()

    class Meta:
        model = PostQA
        fields = ['id', 'boo', 'text', 'pix', 'nvotes_up', 'ncomments', 'created_at']
        read_only_fields = ['id']

    # def get_nvotes_up(self, obj):
    #     return obj._nvotes_up


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        if isinstance(instance, PostVoteOX):
            return {'type':'postvoteox', **PostVoteOXSerializer(instance=instance).data}

        elif isinstance(instance, PostVoteAB):
            return {'type':'postvoteab', **PostVoteABSerializer(instance=instance).data}

        elif isinstance(instance, PostQA):
            return {'type':'postqa', **PostQASerializer(instance=instance).data}

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



def preproc(text, remove_url=True, remove_mention=False, remove_hashtag=False):
    LINEBREAK = r'\n' # str.replace에서는 r'\n'으로 검색이 안된다
    RT = '((?: rt)|(?:^rt))[^ @]?'
    EMOJI = r'[\U00010000-\U0010ffff]'
    DOTS = '…'
    LONG_BLANK = r'[ ]+'
    SPECIALS = r'([^ a-zA-Z0-9_\u3131-\u3163\uac00-\ud7a3]+)|([ㄱ-ㅣ]+)'

    # \u3131-\u3163\uac00-\ud7a3 는 한글을 의미함
    # URL = r'(?P<url>(https?://)?(www[.])?[^ \u3131-\u3163\uac00-\ud7a3]+[.][a-z]{2,6}\b([^ \u3131-\u3163\uac00-\ud7a3]*))'
    URL1 = r'(?:https?:\/\/)?(?:www[.])?[^ :\u3131-\u3163\uac00-\ud7a3]+[.][a-z]{2,6}\b(?:[^ \u3131-\u3163\uac00-\ud7a3]*)'
    URL2 = r'pic.twitter.com/[a-zA-Z0-9_]+'
    URL = '|'.join((URL1, URL2))

    HASHTAG = r'#(?P<inner_hashtag>[^ #@]+)'
    MENTION = r'@(?P<inner_mention>[^ #@]+)'

    text = text.lower()

    if remove_url:
        text = re.sub(URL, ' ', text)

    if remove_mention:
        text = re.sub(MENTION, ' ', text)
    else:
        text = re.sub(MENTION, ' \g<inner_mention>', text)

    if remove_hashtag:
        text = re.sub(HASHTAG, ' ', text)
    else:
        text = re.sub(HASHTAG, ' \g<inner_hashtag>', text)

    text = re.sub('|'.join((LINEBREAK, RT, EMOJI, DOTS, SPECIALS)), ' ', text)
    return re.sub(LONG_BLANK, ' ', text).strip()
