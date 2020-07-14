from django.db import models
from custom_user.models import AbstractEmailUser
from model_utils.managers import InheritanceManager
from vote.models import VoteModel
from datetime import datetime

# Create your models here.

class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractEmailUser):
    boo_selected = models.IntegerField(default=0)

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
    def post_type(self):
        return self.__class__.__name__.lower()

    def vote(self, action, boo_id):
        # up
        if action==0:
            self.votes.up(boo_id)

        # down
        elif action==1:
            self.votes.down(boo_id)

    @property
    def nvotes(self):
        return self.num_vote_up + self.num_vote_down

    def score(self, what, add=0):
        try:
            if what=='up':
                num_vote = self.num_vote_up + add

            elif what=='down':
                num_vote = self.num_vote_down + add

            nvotes = self.nvotes + add
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
    def score_up_fwd(self):
        return self.score('up', add=1)

    @property
    def score_down_fwd(self):
        return self.score('down', add=1)
        

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
