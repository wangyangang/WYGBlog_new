from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q

import mistune

from blog.models import Post
from config.models import BlogSettings


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    content_html = models.TextField(verbose_name='html形式的内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        # return self.content if len(self.content) <= 10 else self.content[:10]
        return self.content[:10]

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)

    @classmethod
    def get_by_blog_name(cls, blog_name):
        return cls.objects.filter(post__blog__name=blog_name, status=cls.STATUS_NORMAL)

    @classmethod
    def get_by_post(cls, post):
        return cls.objects.first(status=cls.STATUS_NORMAL, post=post)

    @classmethod
    def latest_comments(cls, blog_name):
        if not blog_name:
            return None
        else:
            ret = cls.objects.filter(post__blog__name=blog_name, status=cls.STATUS_NORMAL).order_by('-created_time')

            user_settings = BlogSettings.get_dict_by_blog_name(blog_name)  # 用户设置
            display_count = user_settings['sidebar_comment_count']  # 侧边栏评论展示的条数
            return ret[:display_count]
        # return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')



