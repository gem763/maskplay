from django.db import models

# Create your models here.

class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class User(BigIdAbstract):
    pass


class Feed(BigIdAbstract):
    pass


class Post(BigIdAbstract):
    pass


class Store(BigIdAbstract):
    pass


class Pix(BigIdAbstract):
    pass


class Pixtag(BigIdAbstract):
    pass


class MobileVerifier(BigIdAbstract):
    pass


class Brand(BigIdAbstract):
    pass


class Survey(BigIdAbstract):
    pass


class SurveyRecord(BigIdAbstract):
    pass


class Balancegame(BigIdAbstract):
    pass


class BalancegameRecord(BigIdAbstract):
    pass


class Flashgame(BigIdAbstract):
    pass


class FlashgameRecord(BigIdAbstract):
    pass


class Comment(BigIdAbstract):
    pass


class Bookmark(BigIdAbstract):
    pass


class Follow(BigIdAbstract):
    pass


class Hashtag(BigIdAbstract):
    pass
