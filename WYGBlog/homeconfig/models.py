from django.db import models
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse


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
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        categories = cls.objects.filter(status=Category.STATUS_NORMAL)
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


# Create your models here.
class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏')
    )
    DISPLAY_HTML = 1
    DISPLAY_HOT = 2
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_HOT, '最热文章'),
    )
    title = models.CharField('标题', max_length=50, unique=True)
    display_type = models.PositiveIntegerField(default=1,
                                               choices=SIDE_TYPE,
                                               verbose_name='展示类型')
    display_index = models.PositiveIntegerField('展示顺序数字大的靠前', default=1, blank=True)
    content = models.CharField(max_length=500,
                               blank=True,
                               verbose_name='内容',
                               help_text='如果展示的是HTML类型，不可为空')
    status = models.PositiveIntegerField(default=STATUS_SHOW,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
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

        elif self.display_type == self.DISPLAY_HOT:
            hot_posts = Post.hot_posts(None)
            context = {'hot_posts': hot_posts}
            result = render_to_string('homeconfig/blocks/sidebar_posts.html', context)

        return result

    @classmethod
    def get_all(cls):
        """
        获取侧边栏
        (根据博客设置里，是否显示某种侧边栏进行筛选)
        """
        user_settings = BlogSettings.get_dict()
        show_html = user_settings['show_sidebar_html']  # 是否显示侧边栏html
        show_hot_article = user_settings['show_sidebar_hot_article']  # 是否显示最热文章

        sidebars = cls.objects.filter(status=cls.STATUS_SHOW).\
            order_by('-display_index')  # 登录用户的所有侧边栏
        if not show_html:
            # 排除自定义HTML的sidebar
            sidebars = sidebars.exclude(display_type=SideBar.DISPLAY_HTML)
        if not show_hot_article:
            # 排除hot_article的sidebar
            sidebars = sidebars.exclude(display_type=SideBar.DISPLAY_HOT)
        return sidebars

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'


class TopBar(models.Model):
    DISPLAY_URL = 1  # 显示一个链接
    DISPLAY_MY_BLOG = 2  # 我的博客
    DISPLAY_ADMIN = 3  # 管理

    DISPLAY_TYPE = (
        (DISPLAY_URL, '超链接'),
        (DISPLAY_MY_BLOG, '我的博客'),
        (DISPLAY_ADMIN, '管理'),
    )

    name = models.CharField('名称', max_length=20, unique=True)
    display_type = models.PositiveIntegerField('类型', choices=DISPLAY_TYPE, default=1)
    show_type = models.BooleanField('是否显示', default=True)
    display_index = models.PositiveIntegerField('数字越大显示越靠前', default=1)
    content = models.CharField('链接到的地址,超链接必须有内容', max_length=512, null=True, blank=True)
    link = models.CharField('链接,admin里save_model方法自动保存', max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '顶部导航按钮'

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.filter(show_type=True).order_by('-display_index')

    # def save(self, *args, **kwargs):
        # if self.display_type == TopBar.DISPLAY_ADMIN:
        #     self.link = reverse('admin:index')
        # elif self.display_type == TopBar.DISPLAY_MY_BLOG:
        #     self.link = reverse('blog', args=[])
        #     print(self.link)
        # super().save(*args, **kwargs)


class BlogSettings(models.Model):
    """站点配置"""
    site_name = models.CharField('网站名称', max_length=100, null=False,
                                 blank=False, default='Django blog')
    site_description = models.CharField('网站描述', max_length=1000, null=False,
                                        blank=False, default='A new Django blog')
    beian_code = models.CharField('备案号', max_length=100, null=True, blank=True)
    # owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    latest_article_count = models.PositiveIntegerField('最新文章数目', default=5)
    sidebar_hot_article_count = models.PositiveIntegerField('侧边栏最热文章数目', default=5)
    # sidebar_comment_count = models.PositiveIntegerField('侧边栏评论数目', default=5)

    show_sidebar_html = models.BooleanField('是否显示侧边栏html', default=True)
    # show_sidebar_comment = models.BooleanField('是否显示侧边栏评论', default=True)
    show_sidebar_hot_article = models.BooleanField('是否显示侧边栏最热文章', default=True)
    # show_sidebar_latest_article = models.BooleanField('是否显示侧边栏最新文章', default=True)
    index_post_count = models.PositiveIntegerField('首页展示文章条数', default=6)

    class Meta:
        verbose_name = verbose_name_plural = '站点配置'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from WYGBlog.utils import cache
        cache.clear()

    def dict(self):
        dic = dict()
        dic['site_name'] = self.site_name
        dic['site_description'] = self.site_description
        dic['show_sidebar_html'] = self.show_sidebar_html
        dic['show_sidebar_hot_article'] = self.show_sidebar_hot_article
        dic['show_sidebar_latest_article'] = self.latest_article_count
        dic['sidebar_hot_article_count'] = self.sidebar_hot_article_count
        dic['index_post_count'] = self.index_post_count
        return dic

    @classmethod
    def get_dict(cls):
        user_settings = cls.objects.first()
        if user_settings:
            return user_settings.dict()
        else:
            return BlogSettings().dict()