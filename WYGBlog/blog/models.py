from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property

import mistune


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
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

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
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
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须是MARKDOWN格式')
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').only('id', 'title')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.content_html = mistune.markdown(self.content)
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']


    @staticmethod
    def latest_posts():
        return Post.objects.filter(status=Post.STATUS_NORMAL).order_by('-created_time')
