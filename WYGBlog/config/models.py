from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser

from mdeditor.fields import MDTextField


from home.models import Blog


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    title = models.CharField(max_length=50, verbose_name='标题', unique=True)
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    weight = models.PositiveIntegerField(default=1,
                                         choices=zip(range(1, 6), range(1, 6)),
                                         verbose_name='权重',
                                         help_text='权重高展示顺序靠前')
    blog = models.ForeignKey(Blog, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_all_by_blog_name(cls, blog_name):
        return cls.objects.filter(status=cls.STATUS_NORMAL, blog__name=blog_name).order_by('-weight')

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
    display_index = models.PositiveIntegerField('展示顺序(数字大的靠前)', default=1, blank=True)
    title = models.CharField('标题', max_length=50)
    display_type = models.PositiveIntegerField(default=1,
                                               choices=SIDE_TYPE,
                                               verbose_name='展示类型')
    content = models.CharField(max_length=500,
                               blank=True,
                               null=True,
                               verbose_name='展示内容(自定义HTML才需要填)',
                               help_text='展示内容(自定义HTML才需要填)')
    status = models.PositiveIntegerField(default=STATUS_SHOW,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    blog = models.ForeignKey(Blog, verbose_name='作者', on_delete=models.CASCADE)
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
            latest_posts = Post.latest_posts(self.blog.name)
            user_settings = BlogSettings.get_dict_by_blog_name(self.blog.name)  # 用户设置
            display_latest_count = user_settings['sidebar_latest_article_count']  # 侧边栏最新文章展示条数
            context = {'latest_posts': latest_posts, 'display_latest_count': display_latest_count}
            result = render_to_string('config/blocks/sidebar_posts.html', context)

        elif self.display_type == self.DISPLAY_HOTEST:
            hot_posts = Post.hot_posts(self.blog.name)
            context = {'hot_posts': hot_posts}
            result = render_to_string('config/blocks/sidebar_posts.html', context)

        elif self.display_type == self.DISPLAY_COMMENT:
            comments = Comment.latest_comments(self.blog.name)
            context = {'comments': comments}
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        return result

    @classmethod
    def get_all_by_blog_name(cls, blog_name):
        """
        根据用户获取侧边栏，匿名用户显示所有，登录用户显示登录用户的侧边栏
        (还要根据博客设置里，是否显示某种侧边栏进行筛选)
        """
        user_settings = BlogSettings.get_dict_by_blog_name(blog_name)
        show_html = user_settings['show_sidebar_html']  # 是否显示侧边栏html
        show_comment = user_settings['show_sidebar_comment']  # 是否显示评论
        show_latest_article = user_settings['show_sidebar_latest_article']  # 是否显示最新文章
        show_hot_article = user_settings['show_sidebar_hot_article']  # 是否显示最热文章

        user_sidebar = cls.objects.filter(status=cls.STATUS_SHOW, blog__name=blog_name).order_by('-display_index')  # 登录用户的所有侧边栏
        if not show_html:
            # 排除自定义HTML的sidebar
            user_sidebar = user_sidebar.exclude(display_type=SideBar.DISPLAY_HTML)
        if not show_comment:
            # 排除comment的sidebar
            user_sidebar = user_sidebar.exclude(display_type=SideBar.DISPLAY_COMMENT)
        if not show_hot_article:
            # 排除hot_article的sidebar
            user_sidebar = user_sidebar.exclude(display_type=SideBar.DISPLAY_HOTEST)
        if not show_latest_article:
            # 排除latest_article的sidebar
            user_sidebar = user_sidebar.exclude(display_type=SideBar.DISPLAY_LATEST)
        return user_sidebar

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'


class TopBar(models.Model):
    # STATUS_SHOW = 1
    # STATUS_HIDE = 0
    # STATUS_ITEMS = (
    #     (STATUS_SHOW, '显示'),
    #     (STATUS_HIDE, '隐藏')
    # )
    DISPLAY_URL = 1  # 显示一个链接
    DISPLAY_ARCHIVE = 2  # 归档
    DISPLAY_ADMIN = 3  # 管理
    DISPLAY_HOME = 4  # 博客园首页链接
    # DISPLAY_MY_BLOG = 5  # 博客首页
    DISPLAY_LINKS = 5  # 友链
    DISPLAY_ABOUT = 6  # 关于

    DISPLAY_TYPE = (
        (DISPLAY_URL, '超链接'),
        (DISPLAY_ARCHIVE, '归档'),
        (DISPLAY_ADMIN, '管理'),
        (DISPLAY_HOME, '博客园首页'),
        # (DISPLAY_MY_BLOG, '我的博客'),
        (DISPLAY_LINKS, '友链'),
        (DISPLAY_ABOUT, '关于'),
    )

    name = models.CharField('名称', max_length=20)
    display_type = models.PositiveIntegerField('类型', choices=DISPLAY_TYPE, default=1)
    show_type = models.BooleanField('是否显示', default=True)
    display_index = models.PositiveIntegerField('数字越大越靠前', default=1)
    content = models.CharField('内容,超链接必须有内容', max_length=512, null=True, blank=True)
    link = models.CharField('链接', max_length=512, null=True, blank=True)

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '顶部导航按钮'

    def __str__(self):
        return self.name

    @classmethod
    def get_by_blog_name(cls, blog_name):
        return cls.objects.filter(blog__name=blog_name).order_by('-display_index')


class BlogSettings(models.Model):
    """站点配置"""
    site_name = models.CharField('网站名称', max_length=100, null=False,
                                 blank=False, default='Django blog')
    site_description = models.CharField('网站描述', max_length=1000, null=False,
                                        blank=False, default='A new Django blog')
    beian_code = models.CharField('备案号', max_length=100, null=True, blank=True)
    blog = models.ForeignKey(Blog, verbose_name='作者', on_delete=models.CASCADE)

    sidebar_latest_article_count = models.PositiveIntegerField('侧边栏最新文章数目', default=5)
    sidebar_hot_article_count = models.PositiveIntegerField('侧边栏最热文章数目', default=5)
    sidebar_comment_count = models.PositiveIntegerField('侧边栏评论数目', default=5)

    show_sidebar_html = models.BooleanField('是否显示侧边栏html', default=True)
    show_sidebar_comment = models.BooleanField('是否显示侧边栏评论', default=True)
    show_sidebar_hot_article = models.BooleanField('是否显示侧边栏最热文章', default=True)
    show_sidebar_latest_article = models.BooleanField('是否显示侧边栏最新文章', default=True)

    index_post_count = models.PositiveIntegerField('首页文章展示数目', default=8)
    archive_post_count = models.PositiveIntegerField('归档页面文章展示数目', default=10)

    class Meta:
        verbose_name = verbose_name_plural = '站点配置'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from WYGBlog.utils import cache
        cache.clear()

    def get_dict(self):
        dic = dict()
        dic['site_name'] = self.site_name
        dic['site_description'] = self.site_description
        dic['show_sidebar_html'] = self.show_sidebar_html
        dic['show_sidebar_comment'] = self.show_sidebar_comment
        dic['show_sidebar_hot_article'] = self.show_sidebar_hot_article
        dic['show_sidebar_latest_article'] = self.show_sidebar_latest_article
        dic['sidebar_comment_count'] = self.sidebar_comment_count
        dic['sidebar_hot_article_count'] = self.sidebar_hot_article_count
        dic['sidebar_latest_article_count'] = self.sidebar_latest_article_count
        dic['index_post_count'] = self.index_post_count
        dic['archive_post_count'] = self.archive_post_count
        return dic

    @classmethod
    def get_dict_by_blog_name(cls, blog_name):
        user_settings = cls.objects.filter(blog__name=blog_name).first()
        if user_settings:
            return user_settings.get_dict()
        else:
            return BlogSettings().get_dict()


class AboutPage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = MDTextField('正文')

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    pv = models.PositiveIntegerField('阅读数pv', default=1)
    uv = models.PositiveIntegerField('阅读数uv', default=1)

    class Meta:
        verbose_name = verbose_name_plural = 'About页面'

    def __str__(self):
        return 'About页面'
