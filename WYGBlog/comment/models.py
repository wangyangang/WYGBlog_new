from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from blog.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    target = models.CharField(max_length=100, verbose_name='评论目标')
    content = models.TextField(verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.content if len(self.content) <= 10 else self.content[:10]

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)

    @classmethod
    def latest_comments(cls, owner):
        current_user_posts = owner.post_set.all()  # 当前用户的所有文章
        posts_urls = []

        from django.urls import reverse
        for post in current_user_posts:
            posts_urls.append(reverse('blog:post', args=[post.id]))
        ret = cls.objects.filter(status=cls.STATUS_NORMAL)
        ret = ret.filter(Q(target__in=posts_urls) | Q(target__icontains='links'))
        return ret
        # return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')

    class Meta:
        verbose_name = verbose_name_plural = '评论'


