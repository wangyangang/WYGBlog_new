from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.sites.models import Site


class BlogUser(AbstractUser):
    nickname = models.CharField('用户名', max_length=100, null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('user:index')

    def __str__(self):
        return self.username

    def get_full_url(self):
        site = Site.objects.get_current()
        url = 'https://{site}{path}'.format(site.domain, self.get_absolute_url())
        return url

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = '用户'
        get_latest_by = 'id'

