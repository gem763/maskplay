from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
# from vote.models import VoteModel
from siteflags.models import ModelWithFlag, FlagBase
from datetime import datetime, date, timedelta
from django.conf import settings
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.db.models import F, Q, Sum, Count, Case, When, IntegerField, Value
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.functional import classproperty
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.utils.safestring import mark_safe
# from notifications.base.models import AbstractNotification
from notifications.signals import notify
from ordered_model.models import OrderedModel

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

MOIBER_BOO = 97
BOO_DELETED = 97
GUESTBOO = 363

# model_path = os.path.join(settings.BASE_DIR, 'data', 'doc2vec.model')
# d2v = Doc2Vec.load(model_path)

class Identity(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    keywords = models.TextField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name

    # @property
    # def val(self):
    #     return Identity.objects.all()


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


def _labelpix_path(instance, fname):
    _fname = str(datetime.now()) + '__' + fname
    fmt = 'label/{fname}'
    return fmt.format(fname=_fname)


class Label(BigIdAbstract):
    label = models.CharField(max_length=20, null=False, blank=False)
    key = models.IntegerField(default=0)
    pix = models.ImageField(upload_to=_labelpix_path, max_length=500, null=True, blank=True)

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
    @classproperty
    def istylelabels(cls):
        return cls.objects.order_by('key').values_list('id', flat=True)

class Itemlabel(Label):
    @classproperty
    def iitemlabels(cls):
        return cls.objects.order_by('key').values_list('id', flat=True)

class StylelabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stylelabel
        fields = ['id', 'label', 'pix']
        read_only_fields = fields

class ItemlabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itemlabel
        fields = ['id', 'label', 'pix']
        read_only_fields = fields


class MobileVerifier(BigIdAbstract):
    mobile = models.CharField(max_length=20, blank=False, null=False)
    authkey = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.mobile


class User(AbstractEmailUser):
    name = models.CharField(max_length=30, blank=True, null=True)

    GENDER_TYPES = ( (0, '남성'), (1, '여성'), )
    gender = models.IntegerField(choices=GENDER_TYPES, default=0, null=False, blank=False)
    birth = models.DateField(auto_now=False, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    mobile_verified = models.BooleanField(default=False)
    boo_selected = models.IntegerField(default=0)
    help = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        #
        #
        super().save(*args, **kwargs)


    @classmethod
    def guest(cls):
        return cls.objects.get(email=GUEST)

    @property
    def has_active_boo(self):
        return self.boo_set.filter(active=True).count() > 0

    @property
    def boo(self):
        return self.boo_set.get(pk=self.boo_selected)

    @property
    def other_boos(self):
        _boos = self.boo_set.filter(active=True).exclude(pk=self.boo_selected)
        _boos = BooSerializer(_boos, many=True).data
        _boos = {b['id']:b for b in _boos}
        return json.dumps(_boos)

    @property
    def other_boos2(self):
        _boos = self.boo_set.filter(active=True).exclude(pk=self.boo_selected)
        _boos = { boo.id:{'id':boo.id, 'nick':boo.nick } for boo in _boos }
        # _boos = { boo.id:{'id':boo.id, 'nick':boo.nick, 'collections':boo.collections } for boo in _boos }
        return _boos
        # return json.dumps(_boos)


    @property
    def serialized(self):
        _user = UserSerializer(self).data
        return json.dumps(_user)

    @property
    def serialized2(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'gender': self.gender,
            'birth': self.birth,
            'address': self.address,
            'mobile': self.mobile,
            'mobile_verified': self.mobile_verified,
            'is_superuser': self.is_superuser,
            'boo_selected': self.boo_selected,
            'help': self.help,
            'boo': {'id':self.boo.id, 'nick':self.boo.nick }
        }

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
        self.set_boo(max(boos_id))


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



IN_CHECKIN_GAME = 0
IN_DAILY_BALANCE_GAME = 1
IN_DAILY_COLLECTING = 2
IN_RESEARCH = 3
IN_INTERVIEW = 4
IN_WELCOME = 5
IN_BASEINFO_INPUT = 6
IN_STYLELABELS_INPUT = 7
IN_ITEMLABELS_INPUT = 8

OUT_SUPPORT = 100
OUT_RAFFLE = 101
OUT_SHOPPING = 102

class Wallet(BigIdAbstract):
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def send(self, to=None, type=None, amount=None):
        if type == 'checkin_game':
            _type = IN_CHECKIN_GAME

        elif type == 'daily_balance_game':
            _type = IN_DAILY_BALANCE_GAME

        elif type == 'daily_collecting':
            _type = IN_DAILY_COLLECTING

        elif type == 'research':
            _type = IN_RESEARCH

        elif type == 'interview':
            _type = IN_INTERVIEW

        elif type == 'welcome':
            _type = IN_WELCOME

        elif type == 'baseinfo_input':
            _type = IN_BASEINFO_INPUT

        elif type == 'stylelabels_input':
            _type = IN_STYLELABELS_INPUT

        elif type == 'itemlabels_input':
            _type = IN_ITEMLABELS_INPUT

        elif type == 'support':
            _type = OUT_SUPPORT

        elif type == 'raffle':
            _type = OUT_RAFFLE

        elif type == 'shopping':
            _type = OUT_SHOPPING

        Transaction.objects.create(sender=self, receiver=to, type=_type, amount=amount)



    # def write(self, type=None, amount=None):
    #     user = get_current_user()
    #     if not user.is_authenticated:
    #         return
    #
    #     if type == 'checkin_game':
    #         _type = IN_CHECKIN_GAME
    #
    #     elif type == 'daily_balance_game':
    #         _type = IN_DAILY_BALANCE_GAME
    #
    #     elif type == 'daily_collecting':
    #         _type = IN_DAILY_COLLECTING
    #
    #     elif type == 'research':
    #         _type = IN_RESEARCH
    #
    #     elif type == 'interview':
    #         _type = IN_INTERVIEW
    #
    #     elif type == 'welcome':
    #         _type = IN_WELCOME
    #
    #     elif type == 'base_input':
    #         _type = IN_BASE_INPUT
    #
    #     elif type == 'style_input':
    #         _type = IN_STYLE_INPUT
    #
    #     elif type == 'item_input':
    #         _type = IN_ITEM_INPUT
    #
    #     elif type == 'support':
    #         _type = OUT_SUPPORT
    #
    #     elif type == 'raffle':
    #         _type = OUT_RAFFLE
    #
    #     elif type == 'shopping':
    #         _type = OUT_SHOPPING
    #
    #     Transaction.objects.create(wallet=self, type=_type, amount=amount, client=user.boo)

    @property
    def whose(self):
        if hasattr(self, 'boo'):
            return self.boo

        elif hasattr(self, 'raffle'):
            return self.raffle

        elif hasattr(self, 'support'):
            return self.support

    @property
    def whose_type(self):
        _whose = self.whose
        if _whose:
            return _whose.__class__.__name__.lower()

    def __str__(self):
        return str(self.whose)

    @property
    def n_transaction(self):
        return self.sender_transaction_set.count() + self.receiver_transaction_set.count()
        # return self.transaction_set.count()

    @property
    def amount(self):
        return self.inflow - self.outflow
        # agg = self.transaction_set.aggregate(total=Sum('amount'))
        # return agg['total'] if agg['total'] else 0

    @property
    def amount_today(self):
        return self.inflow_today - self.outflow_today
        # agg = self.transaction_set.filter(when__date=datetime.now().date()).aggregate(total=Sum('amount'))
        # return agg['total'] if agg['total'] else 0

    @property
    def amount_daybonus(self):
        q = Q(type=IN_DAILY_BALANCE_GAME) | Q(type=IN_DAILY_COLLECTING)
        agg = self.receiver_transaction_set.filter(q, when__date=datetime.now().date()).aggregate(total=Sum('amount'))
        return agg['total'] if agg['total'] else 0


    @property
    def checkin_today(self):
        return self.receiver_transaction_set.filter(when__date=datetime.now().date(), type=IN_CHECKIN_GAME).exists()
        # return self.transaction_set.filter(when__date=datetime.now().date(), type=IN_CHECKIN_GAME).exists()

    @property
    def welcomed(self):
        return self.receiver_transaction_set.filter(type=IN_WELCOME).exists()
        # return self.transaction_set.filter(type=IN_WELCOME).exists()

    @property
    def baseinfo_inputed(self):
        agg = self.receiver_transaction_set.filter(type=IN_BASEINFO_INPUT).aggregate(total=Sum('amount'))
        return agg['total'] > 0 if agg['total'] else False
        # return self.receiver_transaction_set.filter(type=IN_BASEINFO_INPUT).exists()
        # return self.transaction_set.filter(type=IN_BASE_INPUT).exists()

    @property
    def stylelabels_inputed(self):
        agg = self.receiver_transaction_set.filter(type=IN_STYLELABELS_INPUT).aggregate(total=Sum('amount'))
        return agg['total'] > 0 if agg['total'] else False
        # return self.receiver_transaction_set.filter(type=IN_STYLELABELS_INPUT).exists()
        # return self.transaction_set.filter(type=IN_STYLE_INPUT).exists()

    @property
    def itemlabels_inputed(self):
        agg = self.receiver_transaction_set.filter(type=IN_ITEMLABELS_INPUT).aggregate(total=Sum('amount'))
        return agg['total'] > 0 if agg['total'] else False
        # return self.receiver_transaction_set.filter(type=IN_ITEMLABELS_INPUT).exists()
        # return self.transaction_set.filter(type=IN_ITEM_INPUT).exists()

    # @property
    # def stats(self):
    #     agg = self.transaction_set.values('type').annotate(total=Sum('amount'))
    #     return list(agg)

    @property
    def inflow(self):
        agg = self.receiver_transaction_set.aggregate(total=Sum('amount'))
        # agg = self.transaction_set.aggregate(
        #     total=Sum(Case(
        #         When(amount__gt=0, then=F('amount')),
        #         default=Value(0),
        #         output_field=IntegerField()
        #     ))
        # )
        return agg['total'] if agg['total'] else 0

    @property
    def outflow(self):
        agg = self.sender_transaction_set.aggregate(total=Sum('amount'))
        # agg = self.transaction_set.aggregate(
        #     total=Sum(Case(
        #         When(amount__lt=0, then=F('amount')),
        #         default=Value(0),
        #         output_field=IntegerField()
        #     ))
        # )
        return agg['total'] if agg['total'] else 0

    @property
    def inflow_today(self):
        agg = self.receiver_transaction_set.filter(when__date=datetime.now().date()).aggregate(total=Sum('amount'))
        return agg['total'] if agg['total'] else 0

    @property
    def outflow_today(self):
        agg = self.sender_transaction_set.filter(when__date=datetime.now().date()).aggregate(total=Sum('amount'))
        return agg['total'] if agg['total'] else 0


class Transaction(BigIdAbstract):
    sender = models.ForeignKey(Wallet, related_name='sender_transaction_set', related_query_name='sender_transaction', blank=True, null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(Wallet, related_name='receiver_transaction_set', related_query_name='receiver_transaction', blank=True, null=True, on_delete=models.SET_NULL)
    when = models.DateTimeField(default=timezone.now, null=False)
    # client = models.ForeignKey('Boo', blank=True, null=True, on_delete=models.SET_NULL)

    TRANSACTION_TYPES = (
        (IN_CHECKIN_GAME, '출첵게임'),
        (IN_DAILY_BALANCE_GAME, '매일밸런스게임'),
        (IN_DAILY_COLLECTING, '옷장넣기'),
        (IN_RESEARCH, '리서치참여'),
        (IN_INTERVIEW, '인터뷰참여'),
        (IN_WELCOME, '첫방문환영'),
        (IN_BASEINFO_INPUT, '기본정보입력'),
        (IN_STYLELABELS_INPUT, '관심스타일입력'),
        (IN_ITEMLABELS_INPUT, '관심아이템입력'),

        (OUT_SUPPORT, '후원'),
        (OUT_RAFFLE, '래플'),
        (OUT_SHOPPING, '쇼핑')
    )

    type = models.IntegerField(choices=TRANSACTION_TYPES, default=0, null=False, blank=False)
    amount = models.IntegerField(default=0)

    def __str__(self):
        sender = '-'
        receiver = '-'

        if self.sender:
            sender = str(self.sender)

        if self.receiver:
            receiver = str(self.receiver)

        return sender + ' > ' + receiver


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

    postags = models.JSONField(default=dict, blank=True, null=True)
    negtags = models.JSONField(default=dict, blank=True, null=True)
    coltags = models.JSONField(default=dict, blank=True, null=True)
    # reward_today = models.IntegerField(default=0)

    coltagged = models.BooleanField(default=False)

    contentwork_result = models.JSONField(default=dict, blank=True, null=True)
    researched = models.JSONField(default=list, blank=True, null=True)
    answers = models.JSONField(default=dict, blank=True, null=True)

    wallet = models.OneToOneField(Wallet, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.nick + ' | ' + self.user.email

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

    def answers_of(self, research_id):
        if str(research_id) in self.answers:
            return self.answers[str(research_id)]
        else:
            return {}

    @property
    def icollections(self):
        user = get_current_user()
        if user.is_authenticated and (user.boo.id == self.id) and (self.ncollections == 0):
            Collection.objects.create(owner=self, name=self.nick+'의 옷장')

        return list(self.collection_set.order_by('-order').values_list('id', flat=True))

    @property
    def collections(self):
        # if self.ncollections == 0:
        #     Collection.objects.create(owner=self, name=self.nick+'의 옷장')

        return list(self.collection_set.order_by('-order').values('id', 'name'))

    @property
    def ncollections(self):
        return self.collection_set.count()

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


    @property
    def styleprofile(self):
        try:
            # if not self.coltagged:
            #     _tokens = Pix.objects.filter(pick__collection__owner=self).values_list('tokens', flat=True)
            #     self.coltags = collections.Counter(' '.join(_tokens).split())
            #     self.coltagged = True
            #     self.save()
            #
            #
            # n = 100
            # _basetags = dict(collections.Counter(self.basetags).most_common(n))#; print(_basetags)
            # _coltags = dict(collections.Counter(self.coltags).most_common(n))#; print(_coltags)
            # _postags = dict(collections.Counter(self.postags).most_common(n))#; print(_postags)
            # _negtags = dict(collections.Counter(self.negtags).most_common(n))#; print(_negtags)
            #
            # base_vec = d2v.infer_vector(_basetags, epochs=500)#; print(base_vec)
            # col_vec = d2v.infer_vector(_coltags, epochs=500)#; print(col_vec)
            # pos_vec = d2v.infer_vector(_postags, epochs=500)#; print(pos_vec)
            # neg_vec = d2v.infer_vector(_negtags, epochs=500)#; print(neg_vec)
            #
            # _vec = base_vec + col_vec + pos_vec - neg_vec
            # sim = lambda v: d2v.wv.cosine_similarities(_vec, [d2v.infer_vector(v.split(), epochs=500)])[0]
            # _style = {__id.name:sim(__id.keywords) for __id in Identity.objects.all()}
            #
            # _max = max(_style.values())
            # _min = min(_style.values())
            # scaled = lambda x: round((x-_min)/(_max-_min) * 100)
            #
            # brand_freq = d2v.docvecs.most_similar(positive=[base_vec, col_vec, pos_vec], negative=[neg_vec], topn=10)
            # yourbrands = list(dict(brand_freq).keys())
            #
            # if 'ootd' in yourbrands: yourbrands.remove('ootd')
            # if 'category' in yourbrands: yourbrands.remove('category')
            # if 'fashion' in yourbrands: yourbrands.remove('fashion')
            #
            # return {
            #     'scores': {k:scaled(v) for k,v in _style.items()},
            #     'yourbrands': sorted(yourbrands)
            # }
            return {}

        except:
            return {}


    @property
    def basetags(self):
        genderlabels = list(self.genderlabels.values_list('label', flat=True))
        agelabels = [l.replace(' ', '_') for l in self.agelabels.values_list('label', flat=True)]
        # bodylabels = list(self.bodylabels.values_list('label', flat=True))
        stylelabels = list(self.stylelabels.values_list('label', flat=True))
        itemlabels = list(self.itemlabels.values_list('label', flat=True))

        nick = self.nick.lower()
        text = self.text.lower() if self.text else ''
        return preproc(nick + ' ' + text).split(' ') + genderlabels + agelabels + stylelabels + itemlabels


    def settle(self, n_collected=0, n_voted=0, collect_reward=0, vote_reward=0, checkin_reward=0, bonus_reward=0, nomore_today=None):
        _date = datetime.now().date()
        _reward, _ = Reward.objects.get_or_create(boo=self, date=_date)
        _reward.n_collected += n_collected
        _reward.n_voted += n_voted
        _reward.collect_reward += collect_reward
        _reward.vote_reward += vote_reward
        _reward.checkin_reward += checkin_reward
        _reward.bonus_reward += bonus_reward

        if nomore_today is not None:
            # print(nomore_today, '*************************')
            _reward.nomore_today = nomore_today

        _reward.save()
        return _reward

    @property
    def rewards_history(self):
        _rewards = self.reward_set.all()
        _begin = _rewards.earliest('date').date

        _rewards_hist = {}
        _today = datetime.now().date()

        for _r in _rewards:
            k = (_r.date-_begin).days
            _rewards_hist[k] = {
                'date': str(_r.date),
                'is_today': _r.date == _today,
                'n_action': _r.n_collected + _r.n_voted,
                'action_reward': _r.collect_reward + _r.vote_reward,
                'checkin_reward': _r.checkin_reward,
                'bonus_reward': _r.bonus_reward
            }

        return _rewards_hist


    @property
    def rewards(self):
        _total = self.reward_set.aggregate(
            n_action = Sum( F('n_collected') + F('n_voted') ),
            reward = Sum( F('collect_reward') + F('vote_reward') + F('checkin_reward') + F('bonus_reward') ))

        _total['n_action'] = _total['n_action'] if _total['n_action'] else 0
        _total['reward'] = _total['reward'] if _total['reward'] else 0

        _today = self.settle()
        _today = {
            'n_action': _today.n_collected + _today.n_voted,
            'reward': _today.collect_reward + _today.vote_reward,# + _today.checkin_reward + _today.bonus_reward,
            'nomore_today': _today.nomore_today
            }

        # print(_total)
        return { 'total': _total, 'today': _today, 'history': self.rewards_history }

    # def contentwork_resultize(self, agenda, result):
    def contentwork_resultize(self, id, result):
        self.contentwork_result[id] = result

        if id not in self.researched:
            self.researched.append(id)

        self.save()


def _itempix_path(instance, fname):
    # _id = instance.id  # instance 생성 전이기 때문에 id = None
    _fname = str(datetime.now()) + '__' + fname
    _date = str(instance.created_at.date())
    fmt = 'item/{date}/{fname}'
    return fmt.format(date=_date, fname=_fname)



class Item(BigIdAbstract):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.IntegerField(null=False, blank=False, default=0)
    pix_0 = models.ImageField(upload_to=_itempix_path, max_length=500, null=False, blank=False)
    pix_1 = models.ImageField(upload_to=_itempix_path, max_length=500, null=True, blank=True)
    pix_2 = models.ImageField(upload_to=_itempix_path, max_length=500, null=True, blank=True)
    pix_3 = models.ImageField(upload_to=_itempix_path, max_length=500, null=True, blank=True)
    pix_4 = models.ImageField(upload_to=_itempix_path, max_length=500, null=True, blank=True)
    pix_wide = models.ImageField(upload_to=_itempix_path, max_length=500, null=True, blank=True)
    desc = models.TextField(max_length=1000, blank=True, null=True)
    out_of_stock = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.name) + ' - ' + str(self.price)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'pix_1', 'pix_2', 'pix_3', 'pix_4', 'desc']
        read_only_fields = fields


def _brandpix_path(instance, fname):
    _fname = str(datetime.now()) + '__' + fname
    _bname = instance.name_en
    _id = instance.id
    fmt = 'brand/{bname}/{id}/{fname}'
    return fmt.format(bname=_bname, id=_id, fname=_fname)


class Brand(BigIdAbstract):
    name_en = models.CharField(max_length=50, blank=False, null=False, default='')
    name_kr = models.CharField(max_length=50, blank=False, null=False, default='')
    logo = models.ImageField(upload_to=_brandpix_path, max_length=500, null=True, blank=True)
    coverpix_0 = models.ImageField(upload_to=_brandpix_path, max_length=500, null=True, blank=True)
    coverpix_1 = models.ImageField(upload_to=_brandpix_path, max_length=500, null=True, blank=True)
    coverpix_2 = models.ImageField(upload_to=_brandpix_path, max_length=500, null=True, blank=True)
    coverpix_3 = models.ImageField(upload_to=_brandpix_path, max_length=500, null=True, blank=True)
    coverpix_4 = models.ImageField(upload_to=_brandpix_path, max_length=500, null=True, blank=True)
    established = models.IntegerField(null=True, blank=True)
    origin = models.CharField(max_length=20, blank=True, null=True)
    desc = models.TextField(max_length=500, blank=True, null=True)
    homepage = models.URLField(max_length=200, blank=True, null=True)
    insta = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    youtube = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.name_en + ' | ' + self.name_kr

    @property
    def isupports(self):
        return self.support_set.values_list('id', flat=True)

    @property
    def logo_preview(self):
        if self.logo:
            return mark_safe('<img src="{}" style="height:100px;width:100px;object-fit:cover;" />'.format(self.logo.url))
        return ""


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'coverpix_0', 'coverpix_1', 'coverpix_2', 'coverpix_3', 'coverpix_4', 'established', 'origin', 'desc']
        read_only_fields = fields


class Raffle(BigIdAbstract):
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    deduction = models.IntegerField(null=False, blank=False, default=0)
    listing = models.BooleanField(default=False)
    due = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    wallet = models.OneToOneField(Wallet, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.item) + ' | ' + str(self.created_at)

    @classmethod
    def iraffles(cls, boo=None):
        if (boo):
            return cls.objects.filter(listing=True, wallet__receiver_transaction__sender=boo.wallet).order_by('due').values_list('id', flat=True)

        else:
            return cls.objects.filter(listing=True).order_by('due').values_list('id', flat=True)


class RaffleSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = Raffle
        fields = ['id', 'item', 'deduction', 'due', 'wallet']
        read_only_fields = fields

    def get_wallet(self, obj):
        if not obj.wallet:
            obj.wallet = Wallet.objects.create()
            obj.save()

        amount = obj.wallet.amount
        n_transaction = obj.wallet.n_transaction

        user = get_current_user()
        if user.is_authenticated:
            raffled = obj.wallet.receiver_transaction_set.filter(sender=user.boo.wallet).exists()
        else:
            raffled = False

        return {
            'collected': amount, # if amount else 0,
            'n_transaction': n_transaction, # if n_transaction else 0,
            'raffled': raffled
        }

    def get_item(self, obj):
        return {
            'id': obj.item.id,
            'name': obj.item.name,
            'pix_wide': obj.item.pix_wide.url if obj.item.pix_wide else None,
            'pix_0': obj.item.pix_0.url,
            'price': obj.item.price,
            'out_of_stock': obj.item.out_of_stock
        }



class Coffeecoupon(BigIdAbstract):
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    listing = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.item) + ' | ' + str(self.created_at)

    @classproperty
    def icoffeecoupons(cls):
        return cls.objects.filter(listing=True).order_by('item__price').values_list('id', flat=True)


class CoffeecouponSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Coffeecoupon
        fields = ['id', 'item']
        read_only_fields = fields

    def get_item(self, obj):
        return {'id': obj.item.id, 'name': obj.item.name, 'pix_0': obj.item.pix_0.url, 'price': obj.item.price, 'out_of_stock': obj.item.out_of_stock}


class Shoptem(BigIdAbstract):
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    listing = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.item) + ' | ' + str(self.created_at)

    @classproperty
    def ishoptems(cls):
        return cls.objects.filter(listing=True).order_by('item__price').values_list('id', flat=True)


class ShoptemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Shoptem
        fields = ['id', 'item']
        read_only_fields = fields

    def get_item(self, obj):
        return {'id': obj.item.id, 'name': obj.item.name, 'pix_0': obj.item.pix_0.url, 'price': obj.item.price, 'out_of_stock': obj.item.out_of_stock}


class Support(BigIdAbstract):
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    gift = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    ticketsize = models.IntegerField(null=True, blank=True)
    target = models.IntegerField(null=True, blank=True)
    desc = models.TextField(max_length=200, blank=True, null=True)
    due = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    wallet = models.OneToOneField(Wallet, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.brand) + ' | ' + str(self.created_at)

    @classmethod
    def isupports(cls, boo=None):
        if (boo):
            return cls.objects.filter(wallet__receiver_transaction__sender=boo.wallet).order_by('due').values_list('id', flat=True)
        else:
            return cls.objects.order_by('due').values_list('id', flat=True)



class SupportSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    gift = serializers.SerializerMethodField()
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ['id', 'brand', 'active', 'ticketsize', 'target', 'desc', 'due', 'gift', 'wallet']
        read_only_fields = fields

    def get_brand(self, obj):
        if obj.brand:
            return {
                'id': obj.brand.id,
                'logo': obj.brand.logo.url if obj.brand.logo else None,
                'name_en': obj.brand.name_en,
                'name_kr': obj.brand.name_kr,
                'homepage': obj.brand.homepage,
                'insta': obj.brand.insta
            }

    def get_wallet(self, obj):
        if not obj.wallet:
            obj.wallet = Wallet.objects.create()
            obj.save()

        amount = obj.wallet.amount
        n_transaction = obj.wallet.n_transaction

        user = get_current_user()
        if user.is_authenticated:
            supported = obj.wallet.receiver_transaction_set.filter(sender=user.boo.wallet).exists()
        else:
            supported = False

        return {
            'collected': amount, # if amount else 0,
            'n_transaction': n_transaction, # if n_transaction else 0,
            'supported': supported
        }

    def get_gift(self, obj):
        return {
            'name': obj.gift.name,
            'price': obj.gift.price,
            'pix_0': obj.gift.pix_0.url if obj.gift.pix_0 else None,
            'pix_1': obj.gift.pix_1.url if obj.gift.pix_1 else None,
            'pix_2': obj.gift.pix_2.url if obj.gift.pix_2 else None,
            'pix_3': obj.gift.pix_3.url if obj.gift.pix_3 else None,
            'pix_4': obj.gift.pix_4.url if obj.gift.pix_4 else None,
            'desc': obj.gift.desc
        }


def _coverpix_path(instance, fname):
    try:
        _user = instance.owner.user.email
    except:
        _user = 'anonymous'

    _date = str(instance.created_at.date())
    _fname = str(datetime.now()) + '__' + fname
    fmt = 'research/{user}/{date}/{fname}'
    return fmt.format(user=_user, date=_date, fname=_fname)


class Research(BigIdAbstract):
    owner = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, blank=True, null=True)
    desc = models.TextField(max_length=200, blank=True, null=True)
    published = models.BooleanField(default=False)
    coverpix = models.ImageField(upload_to=_coverpix_path, max_length=500, null=True, blank=True)
    reward = models.IntegerField(default=0)
    due = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.title

    @property
    def coverpix_preview(self):
        if self.coverpix:
            return mark_safe('<img src="{}" style="height:100px;width:170px;object-fit:cover;" />'.format(self.coverpix.url))
        return ""

    @classproperty
    def iresearches(cls):
        return cls.objects.order_by('-priority').values_list('id', flat=True)
        # return cls.objects.filter(published=True).order_by('due').values_list('id', flat=True)

    # @classproperty
    # def iresearches_onwork(cls):
    #     return cls.objects.filter(published=False).order_by('due').values_list('id', flat=True)

    @property
    def iresearchitems(self):
        return self.researchitem_set.order_by('order').values_list('id', flat=True)



class ResearchSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Research
        fields = ['id', 'owner', 'brand', 'title', 'desc', 'published', 'coverpix', 'reward', 'due', 'created_at', 'answers']
        read_only_fields = fields

    def get_owner(self, obj):
        return {'id': obj.owner.id, 'nick': obj.owner.nick}

    def get_answers(self, obj):
        user = get_current_user()
        if user.is_authenticated:
            return user.boo.answers_of(obj.id)
        else:
            return {}

    def get_brand(self, obj):
        if obj.brand:
            return {
                'id': obj.brand.id,
                'logo': obj.brand.logo.url if obj.brand.logo else None,
                'name_en': obj.brand.name_en,
                'name_kr': obj.brand.name_kr,
                'homepage': obj.brand.homepage,
                'insta': obj.brand.insta
            }




def _researchitempix_path(instance, fname):
    try:
        _user = instance.research.owner.user.email
    except:
        _user = 'anonymous'

    try:
        _date = str(instance.research.created_at.date())
    except:
        _date = str(datetime.now().date())

    _fname = str(datetime.now()) + '__' + fname
    fmt = 'research/{user}/{date}/items/{fname}'
    return fmt.format(user=_user, date=_date, fname=_fname)


class ResearchItem(BigIdAbstract, ModelWithFlag):
    research = models.ForeignKey(Research, blank=True, null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    TYPE_KEYS = ( ('AB', 'AB타입'), ('OX', 'OX타입'), ('QA', '주관식'), ('MC', '다중선택형'), ('IN', 'INTRO'), ('OUT', 'OUTRO') )
    type = models.CharField(max_length=3, choices=TYPE_KEYS, default='AB', null=False, blank=False)

    GENDER_KEYS = ( ('X', 'X'), ('M', 'M'), ('F', 'F') )
    gender = models.CharField(max_length=1, choices=GENDER_KEYS, default='X', null=False, blank=False)

    preq = models.BooleanField(default=False)
    text = models.TextField(max_length=100, blank=True, null=True)

    pix_0 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    pixlabel_0 = models.CharField(max_length=20, blank=True, null=True)

    pix_1 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    pixlabel_1 = models.CharField(max_length=20, blank=True, null=True)

    # multi_choices = models.TextField(max_length=200, blank=True, null=True)

    mcpix_0 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_0 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_1 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_1 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_2 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_2 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_3 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_3 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_4 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_4 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_5 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_5 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_6 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_6 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_7 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_7 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_8 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_8 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_9 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_9 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_10 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_10 = models.CharField(max_length=20, blank=True, null=True)

    mcpix_11 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    mclabel_11 = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.type + ((' | ' + str(self.text)) if self.text else '')



class ResearchItemSerializer(serializers.ModelSerializer):
    pix = serializers.SerializerMethodField()
    mc = serializers.SerializerMethodField()

    class Meta:
        model = ResearchItem
        fields = ['id', 'order', 'type', 'gender', 'preq', 'text', 'pix', 'mc']
        read_only_fields = fields

    def get_pix(self, obj):
        if obj.type == 'AB':
            return { 'pix_0': obj.pix_0.url, 'pixlabel_0': obj.pixlabel_0, 'pix_1': obj.pix_1.url, 'pixlabel_1': obj.pixlabel_1 }

        elif obj.type == 'OX':
            return { 'pix_0': obj.pix_0.url }

        elif obj.type == 'QA':
            if obj.pix_0:
                return { 'pix_0': obj.pix_0.url }

        elif obj.type == 'MC':
            if obj.pix_0:
                return { 'pix_0': obj.pix_0.url }

        elif obj.type == 'IN':
            return { 'pix_0': obj.pix_0.url }

        elif obj.type == 'OUT':
            return { 'pix_0': obj.pix_0.url }


    def get_mc(self, obj):
        if obj.type == 'MC':
            _mc = []

            for i in range(12):
                __mclabel = getattr(obj, 'mclabel_' + str(i))
                __mcpix = getattr(obj, 'mcpix_' + str(i))

                # 이미지필드가 비어있는지 확인하는 방법
                # https://stackoverflow.com/questions/5213025/how-to-check-imagefield-is-empty
                if (__mclabel is None) and (not bool(__mcpix)):
                    break

                else:
                    if bool(__mcpix):
                        __mcpix = __mcpix.url

                    else:
                        __mcpix = None

                    _mc.append({ 'mclabel': __mclabel, 'mcpix': __mcpix})

            return _mc


class Flashgame(BigIdAbstract, ModelWithFlag):
    TYPE_KEYS = ( ('AB', 'AB타입'), )
    type = models.CharField(max_length=3, choices=TYPE_KEYS, default='AB', null=False, blank=False)
    text = models.TextField(max_length=100, blank=True, null=True)

    published = models.BooleanField(default=False)
    reward = models.IntegerField(default=10)

    GENDER_KEYS = ( ('X', 'X'), ('M', 'M'), ('F', 'F') )
    gender = models.CharField(max_length=1, choices=GENDER_KEYS, default='X', null=False, blank=False)

    pix_0 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    pixlabel_0 = models.CharField(max_length=20, blank=True, null=True)

    pix_1 = models.ImageField(upload_to=_researchitempix_path, max_length=500, null=True, blank=True)
    pixlabel_1 = models.CharField(max_length=20, blank=True, null=True)

    pub_date = models.DateField(default=timezone.now, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.type + ((' | ' + str(self.text)) if self.text else '')

    @classproperty
    def iflashgames(cls):
        return cls.objects.filter(published=True, pub_date__lte=datetime.now().date()).order_by('-pub_date').values_list('id', flat=True)


class FlashgameSerializer(serializers.ModelSerializer):
    pix = serializers.SerializerMethodField()

    class Meta:
        model = Flashgame
        fields = ['id', 'type', 'gender', 'text', 'pix', 'reward', 'pub_date']
        read_only_fields = fields

    def get_pix(self, obj):
        if obj.type == 'AB':
            return { 'pix_0': obj.pix_0.url, 'pixlabel_0': obj.pixlabel_0, 'pix_1': obj.pix_1.url, 'pixlabel_1': obj.pixlabel_1 }


class Contentwork(BigIdAbstract):
    owner = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    agenda = models.CharField(max_length=30, null=False, blank=False)
    profiles = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agenda

    @classmethod
    def ipostages(cls, id):
    # def ipostages(cls, agenda):
        return Postage.objects.filter(contentwork_id=id).values_list('id', flat=True)

    @property
    def serialized(self):
        _cwork = {
            'id': self.id,
            'agenda': self.agenda,
            'profiles': self.profiles,
        }

        return _cwork


def _postagepix_path(instance, fname):
    try:
        agenda = instance.contentwork.agenda
    except:
        agenda = 'default'

    now = datetime.now()
    fname = str(now) + '__' + fname
    fmt = 'postage/{agenda}/{fname}'
    return fmt.format(agenda=agenda, fname=fname)


class Postage(BigIdAbstract, ModelWithFlag):
    contentwork = models.ForeignKey(Contentwork, blank=True, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    pix_a = models.ImageField(upload_to=_postagepix_path, max_length=500, null=False, blank=False)
    pix_b = models.ImageField(upload_to=_postagepix_path, max_length=500, null=True, blank=True)

    pixlabel_a = models.TextField(max_length=200, blank=True, null=True)
    pixlabel_b = models.TextField(max_length=200, blank=True, null=True)

    group = models.CharField(max_length=30, null=False, blank=False)
    order = models.IntegerField(default=0)


    def __str__(self):
        return self.group + ' | ' + self.text + ((' | ' + str(self.contentwork)) if self.contentwork else '')


    def contentvote(self, action, boo, note=''):
        # up
        if action==VOTE_UP:
            Flager.vote_up(self, boo, note)

        # down
        elif action==VOTE_DOWN:
            Flager.vote_down(self, boo, note)

        # clear
        else:
            Flager.vote_clear(self, boo, note)



class Reward(BigIdAbstract):
    boo = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=timezone.now, null=False)
    n_collected = models.IntegerField(default=0)
    n_voted = models.IntegerField(default=0)
    collect_reward = models.IntegerField(default=0)
    vote_reward = models.IntegerField(default=0)
    checkin_reward = models.IntegerField(default=0)
    bonus_reward = models.IntegerField(default=0)
    nomore_today = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date) + ' ' + str(self.boo)

    class Meta:
        constraints =  [
            models.UniqueConstraint(
                fields=['boo', 'date'],
                name='daily unique reward'
            )
        ]


class Post(BigIdAbstract, ModelWithFlag):
    boo = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_DEFAULT, default=BOO_DELETED)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    group = models.TextField(max_length=200, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    objects = InheritanceManager()


    def __str__(self):
        return str(self.created_at) + ((' | ' + str(self.boo)) if self.boo else '')

    def save(self, *args, **kwargs):
        # 아래 두줄의 순서가 중요할까?
        super().save(*args, **kwargs)
        self.boo.save()

    @classmethod
    def iposts(cls, type):
        if type == 'history':
            excl = Q(boo_id=BOO_DELETED) | Q(boo__hidden=True)
            return Post.objects.exclude(excl).order_by('-created_at').values_list('id', flat=True)

        elif type == 'hot':
            q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
            excl = Q(boo_id=BOO_DELETED) | Q(boo__hidden=True)
            iposts_excl = Post.objects.filter(excl).values_list('id', flat=True)
            ago_2w = datetime.now() - timedelta(days=7)
            return Flager.objects.filter(q, time_created__gte=ago_2w).exclude(object_id__in=iposts_excl).values('object_id').annotate(nvotes=Count('object_id')).order_by('-nvotes').values_list('object_id', flat=True)
            # return Post.objects.exclude(excl).annotate(ordering=F('nvotes_up') + F('nvotes_down')).order_by('-ordering').values_list('id', flat=True)

    @classmethod
    def mbti_iposts(cls, type):
        excl = Q(boo_id=BOO_DELETED)
        return Post.objects.filter(group__startswith='mbti-'+type).exclude(excl).order_by('id').values_list('id', flat=True)


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


def _pixpath(instance, fname):
    try:
        user = instance.owner.user.email
    except:
        user = 'anonymous'

    now = datetime.now()
    fname = str(now) + '__' + fname
    # fmt = 'pix/{year}/{month}/{day}/{user}/{fname}'
    fmt = 'user/{user}/pix/{fname}'
    return fmt.format(user=user, fname=fname)


class Pix(BigIdAbstract):
    owner = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    src = models.ImageField(upload_to=_pixpath, max_length=500, null=False, blank=False)
    desc = models.TextField(max_length=200, blank=True, null=False, default='')
    tokens = models.TextField(max_length=1000, blank=True, null=False, default='')
    outlink = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    TYPE_KEYS = ( ('X', '없음'), ('M', '남자착장'), ('F', '여자착장'), ('T', '아이템') )
    type = models.CharField(max_length=1, choices=TYPE_KEYS, default='F', null=False, blank=False)

    @classmethod
    def ipixs(cls):
        excl = Q(owner__hidden=True)
        return Pix.objects.exclude(excl).values_list('id', flat=True)
        # return Pix.objects.exclude(excl).order_by('-created_at').values_list('id', flat=True)

    def __str__(self):
        return self.desc

    @property
    def preview(self):
        if self.src:
            return mark_safe('<img src="{}" style="height:150px;width:150px;object-fit:cover;" />'.format(self.src.url))
        return ""


class PixSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Pix
        fields = ['id', 'owner', 'src', 'desc', 'outlink']
        read_only_fields = fields

    def get_owner(self, obj):
        return {'id': obj.owner.id, 'nick': obj.owner.nick}
        # return {'id': obj.owner.id, 'nick': obj.owner.nick, 'collections': list(obj.owner.collection_set.order_by('-order').values('id', 'name'))}


class Collection(OrderedModel):
    owner = models.ForeignKey(Boo, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.TextField(max_length=200, blank=False, null=False, default='옷장이름')
    desc = models.TextField(max_length=200, blank=True, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    order_with_respect_to = 'owner'

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.name + (' | ' + str(self.owner)) if self.owner else ''

    @classmethod
    def icols(cls):
        # _icols = Pick.objects.filter(collection__isnull=False).exclude(collection__name__contains='님의 옷장').values_list('collection_id', flat=True)
        _icols = cls.objects.annotate(npicks=Count('pick')).filter(npicks__gte=5).values_list('id', flat=True)
        return list(set(_icols))

    @property
    def npicks(self):
        return self.pick_set.count()

    @property
    def ipicks(self):
        return list(self.pick_set.order_by('-order').values_list('id', flat=True))

    @property
    def serialized(self):
        _serialized = self.serialized_base
        user = get_current_user()

        if user.is_authenticated and (user.boo.id == self.owner.id):
            _pixids = Pix.objects.filter(pick__collection_id=self.id).values_list('id', flat=True)
            _serialized['pixids'] = list(_pixids)

        return _serialized

    @property
    def serialized_base(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': {'id':self.owner.id, 'nick':self.owner.nick }
            # 'owner': {'id':self.owner.id, 'nick':self.owner.nick, 'collections':self.owner.collections }
            }


# class CollectionSerializer(serializers.ModelSerializer):
#     picks = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Collection
#         fields = ['id', 'name', 'picks']
#         read_only_fields = fields
#
#     def get_picks(self, obj):
#         return {'id': obj.owner.id, 'nick': obj.owner.nick, 'collections': list(obj.owner.collection_set.order_by('-order').values('id', 'name'))}


class Pick(OrderedModel):
    pix = models.ForeignKey(Pix, null=False, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True) #
    order_with_respect_to = 'collection'

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return str(self.collection) + ' | ' + str(self.pix)

    @property
    def serialized(self):
        return PickSerializer(self).data


class PickSerializer(serializers.ModelSerializer):
    # pix = PixSerializer(required=False)
    pix = serializers.SerializerMethodField()

    class Meta:
        model = Pick
        fields = ['id', 'pix']
        read_only_fields = fields

    def get_pix(self, obj):
        return {'id': obj.pix.id}



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
    # links = serializers.SerializerMethodField()

    class Meta:
        model = Boo
        # fields = ['id', 'nick', 'text', 'profile', 'active', 'nfollowers', 'nposts', 'genderlabels', 'agelabels', 'bodylabels', 'stylelabels', 'itemlabels', 'links']#, 'collections']
        fields = ['id', 'nick', 'text', 'profile', 'nfollowers']
        read_only_fields = fields

    def get_profile(self, obj):
        return {'pix': obj.profile.pix.url}

    # def get_links(self, obj):
    #     return list(obj.links.filter(user_id=obj.user.id).values_list('url', flat=True))


class GuestbooSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    voting_record = serializers.SerializerMethodField()
    # ilikes_comment = serializers.SerializerMethodField()

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'voting_record']#, 'ilikes_comment']
        read_only_fields = fields

    def get_profile(self, obj):
        return {'pix': obj.profile.pix.url}

    def get_voting_record(self, obj):
        q = Q(status=VOTE_UP) | Q(status=VOTE_DOWN)
        return {f.object_id:f.status for f in Flager.objects.filter(q, user=obj, note=self.context.get('sessionkey'))}

    # def get_ilikes_comment(self, obj):
    #     return list(Flager.objects.filter(status=LIKE_COMMENT, user=obj, note=self.context.get('sessionkey')).values_list('object_id', flat=True))


class BooSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = Boo
        fields = ['id', 'nick', 'text', 'profile', 'genderlabels', 'stylelabels', 'itemlabels', 'researched', 'wallet']
        # fields = ['id', 'nick', 'text', 'profile', 'genderlabels', 'stylelabels', 'itemlabels', 'rewards', 'researched', 'wallet']
        # fields = ['id', 'nick', 'text', 'profile', 'followees_id', 'voting_record', 'genderlabels', 'agelabels', 'bodylabels', 'stylelabels', 'itemlabels', 'rewards', 'researched']
        read_only_fields = ['id']

    def get_wallet(self, obj):
        if not obj.wallet:
            obj.wallet = Wallet.objects.create()
            obj.save()

        return {
            'id': obj.wallet.id,
            'amount': obj.wallet.amount,
            'amount_daybonus': obj.wallet.amount_daybonus,
            # 'amount_today': obj.wallet.amount_today,
            'checkin_today': obj.wallet.checkin_today,
            'welcomed': obj.wallet.welcomed,
            'baseinfo_inputed': obj.wallet.baseinfo_inputed,
            'stylelabels_inputed': obj.wallet.stylelabels_inputed,
            'itemlabels_inputed': obj.wallet.itemlabels_inputed,
        }

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


# class UserSerializer2(serializers.ModelSerializer):
#     boo = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'boo_selected', 'boo']
#         read_only_fields = fields
#
#     def get_boo(self, obj):
#         return {'id': obj.boo.id, 'nick': obj.boo.nick, 'collections': list(obj.boo.collection_set.order_by('-order').values('id', 'name'))}


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
            return { 'img': obj.commentpix_set.first().img.url }
        except:
            pass


class PostageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postage
        fields = ['id', 'text', 'pix_a', 'pix_b', 'pixlabel_a', 'pixlabel_b', 'created_at', 'group', 'order']
        read_only_fields = fields


class PostVoteOXSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()

    class Meta:
        model = PostVoteOX
        fields = ['id', 'boo', 'text', 'pix', 'keys', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at', 'group']
        read_only_fields = ['id', 'nvotes_up', 'nvotes_down']


class PostVoteABSerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()

    class Meta:
        model = PostVoteAB
        fields = ['id', 'boo', 'text', 'pix_a', 'pix_b', 'pixlabel_a', 'pixlabel_b', 'nvotes_up', 'nvotes_down', 'ncomments', 'created_at', 'group']
        read_only_fields = ['id', 'nvotes_up', 'nvotes_down']


class PostQASerializer(serializers.ModelSerializer):
    boo = BasebooSerializer()

    class Meta:
        model = PostQA
        fields = ['id', 'boo', 'text', 'pix', 'nvotes_up', 'ncomments', 'created_at', 'group']
        read_only_fields = ['id']


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
