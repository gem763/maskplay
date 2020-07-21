from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
from vote.models import VoteModel
from datetime import datetime
from django_currentuser.middleware import get_current_user, get_current_authenticated_user

# Create your models here.

class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractEmailUser):
    boo_selected = models.IntegerField(default=0)

    @property
    def boo(self):
        return Boo.objects.get(pk=self.boo_selected, user=self)

    def set_boo(self, boo_id):
        self.boo_selected = boo_id
        self.save()


class Boo(BigIdAbstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100)
    text = models.TextField(max_length=500, blank=True, null=True)
    profile_selected = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nick + ' | ' + self.user.email

    def profile(self):
        return Profile.objects.get(pk=self.profile_selected, boo=self)


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

    def score(self, what, alpha=0, beta=0):
        try:
            if what=='up':
                num_vote = self.num_vote_up + alpha

            elif what=='down':
                num_vote = self.num_vote_down + alpha

            nvotes = self.nvotes + beta
            return int(num_vote / nvotes * 100)

        except:
            return 0

    @property
    def score_up(self):
        return self.score('up')

    @property
    def score_down(self):
        return self.score('down')

    @property
    def score_up_new(self):
        return self.score('up', alpha=1, beta=1)

    @property
    def score_down_new(self):
        return self.score('down', alpha=1, beta=1)

    @property
    def score_up_change(self):
        return self.score('up', alpha=1)

    @property
    def score_down_change(self):
        return self.score('down', alpha=1)


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
