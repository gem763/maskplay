from django.db import models
from custom_user.models import AbstractEmailUser
from datetime import datetime

# Create your models here.

class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractEmailUser):
    pass


class Boo(BigIdAbstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100)
    text = models.TextField(max_length=500, blank=True, null=True)
    profile_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nick + ' | ' + self.user.email

    def profile(self):
        return Profile.objects.get(pk=self.profile_id, boo=self)


def _profilepix_path(instance, fname):
    user = instance.boo.user.email
    fname = str(datetime.now()) + '__' + fname
    fmt = '{user}/{fname}'
    return fmt.format(user=user, fname=fname)


class Profile(BigIdAbstract):
    boo = models.ForeignKey(Boo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    pix = models.ImageField(upload_to=_profilepix_path, max_length=500, null=True, blank=True)

    def __str__(self):
        return self.boo.nick + ' | ' + self.boo.user.email


class Post(BigIdAbstract):
    boo = models.ForeignKey(Boo, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PostVoteOX(Post):
    pass
    # pix_intro = models.ImageField(upload_to=_image_path, max_length=500, null=True, black=True)


class PostVoteAB(Post):
    pass
