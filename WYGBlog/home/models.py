from django.db import models

from django.contrib.auth.models import User
from django.conf import settings


class Blog(models.Model):
    name = models.CharField('博客名', max_length=20, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='blog', on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '博客'

    def __str__(self):
        return self.name

