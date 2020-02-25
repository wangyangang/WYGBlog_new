from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser, User

import markdown
import mistune

from config.models import BlogSettings
from homeconfig.models import BlogSettings as SiteSettings
from mdeditor.fields import MDTextField

from home.models import Blog
from homeconfig.models import Category as Site_Category


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=50, verbose_name='名称', unique=True)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    blog = models.ForeignKey(Blog, verbose_name='所属博客', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_by_blog_name(cls, blog_name):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL, blog__name=blog_name)
        nav_categories = []
        normal_categories = []

        for category in categories:
            if category.is_nav:
                nav_categories.append(category)
            else:
                normal_categories.append(category)

        return {
            'nav_categories': nav_categories,
            'normal_categories': normal_categories
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=10, verbose_name='名称', unique=True)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL,
                                         verbose_name='状态')
    blog = models.ForeignKey(Blog, verbose_name='所属博客', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿')
    )
    title = models.CharField(max_length=255, verbose_name='标题', unique=True)
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要', null=True)
    # content = models.TextField(verbose_name='正文', help_text='正文必须是MARKDOWN格式')
    content = MDTextField('正文')
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.DO_NOTHING)
    site_category = models.ForeignKey(Site_Category, verbose_name='网站分类',
                                      on_delete=models.DO_NOTHING, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='标签', null=True, blank=True)
    blog = models.ForeignKey(Blog, verbose_name='所属博客', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    @classmethod
    def hot_posts(cls, blog_name=None):
        if blog_name:
            user_settings = BlogSettings.get_dict_by_blog_name(blog_name)  # 用户设置
            display_hot_count = user_settings['sidebar_hot_article_count']  # 侧边栏最热文章展示条数
            posts = cls.objects.filter(status=cls.STATUS_NORMAL, blog__name=blog_name).order_by('-pv').only('id',
                                                                                                            'title')
        else:
            site_settings = SiteSettings.get_dict()
            display_hot_count = site_settings['sidebar_hot_article_count']
            posts = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').only('id', 'title', 'pv')
        return posts[:display_hot_count]

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))

    @staticmethod
    def latest_posts(blog_name=None):
        if blog_name:
            # user_settings = BlogSettings.get_dict_by_blog_name(blog_name)  # 用户设置
            # display_latest_count = user_settings['sidebar_latest_article_count']  # 侧边栏最新文章展示条数
            # user_blog = Blog.objects.get(name=blog_name)
            posts = Post.objects.filter(status=Post.STATUS_NORMAL, blog__name=blog_name).order_by('-created_time')
            # return posts[:display_latest_count]
            return posts
        else:  # 所有文章里的最新的
            posts = Post.objects.filter(status=Post.STATUS_NORMAL).order_by('-created_time')
            return posts

    @classmethod
    def sidebar_latest_posts(cls, user):
        posts = Post.objects.filter(status=Post.STATUS_NORMAL, owner=user).order_by('-created_time')
        user_settings = BlogSettings.get_dict_by_user(user)  # 用户设置
        display_count = user_settings['sidebar_latest_article_count']  # 侧边栏最新文章展示的条数
        return posts[:display_count]

    def get_absolute_url(self):
        return reverse('blog:post', args=(self.blog.name, self.id,))

    def save(self, *args, **kwargs):
        self.content_html = markdown.markdown(self.content,
                                              extensions=[
                                                  'markdown.extensions.extra',
                                                  'markdown.extensions.codehilite',
                                                  'markdown.extensions.toc'
                                              ])
        super().save(*args, **kwargs)
