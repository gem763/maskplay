from django.db import models
from custom_user.models import AbstractEmailUser

# Create your models here.

class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class User(AbstractEmailUser):
    pass
