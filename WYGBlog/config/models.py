from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    weight = models.PositiveIntegerField(default=1,
                                         choices=zip(range(1, 6), range(1, 6)),
                                         verbose_name='权重',
                                         help_text='权重高展示顺序靠前')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_all_by_user(cls, user):
        return cls.objects.filter(status=cls.STATUS_NORMAL, owner=user)

    class Meta:
        verbose_name = verbose_name_plural = '友链'


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏')
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOTEST = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOTEST, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    )
    title = models.CharField('标题', max_length=50)
    display_type = models.PositiveIntegerField(default=1,
                                               choices=SIDE_TYPE,
                                               verbose_name='展示类型')
    content = models.CharField(max_length=500,
                               blank=True,
                               verbose_name='内容',
                               help_text='如果展示的部署HTML类型，不可为空')
    status = models.PositiveIntegerField(default=STATUS_SHOW,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.title

    @property
    def content_html(self):
        """直接渲染模板"""
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            return self.content
        elif self.display_type == self.DISPLAY_LATEST:
            posts = Post.latest_posts(self.owner)
            posts = posts if posts.count() <= 7 else posts[:7]
            context = {'posts': posts}
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOTEST:
            print(self.owner)
            context = {'posts': Post.hot_posts(self.owner)}
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            comments = Comment.latest_comments(self.owner)
            comments = comments if comments.count() <= 7 else comments[:7]
            context = {'comments': comments}
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        return result

    @classmethod
    def get_all_by_user(cls, user):

        return cls.objects.filter(status=cls.STATUS_SHOW, owner=user)

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'


class TopBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '显示'),
        (STATUS_HIDE, '隐藏')
    )
    DISPLAY_URL = 1  # 显示一个链接
    DISPLAY_ARCHIVE = 2  # 归档
    DISPLAY_MY_BLOG = 3  # 我的博客
    DISPLAY_ADMIN = 4  # 管理
    DISPLAY_HOME = 5  # 首页链接

    DISPLAY_TYPE = (
        (DISPLAY_URL, '超链接'),
        (DISPLAY_MY_BLOG, '我的博客'),
        (DISPLAY_ARCHIVE, '归档'),
        (DISPLAY_ADMIN, '管理'),
    )




