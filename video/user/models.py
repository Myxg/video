from django.db import models

# Create your models here.


class UserInfo(models.Model):
    objects = None
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=20)
    pow = models.CharField(max_length=20)

    class Meta:
        db_table = 'userinfo'
