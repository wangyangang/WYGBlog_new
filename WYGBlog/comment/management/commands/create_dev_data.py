"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/28/20 - 5:40 PM
"""
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from user.models import BlogUser
from home.models import Blog
from homeconfig.models import TopBar as SiteTopbar, Category as SiteCategory, SideBar as SiteSidebar
from config.models import TopBar, SideBar
from blog.models import Category


class Command(BaseCommand):
    """创建一些测试数据"""
    help = 'create dev data'

    def handle(self, *args, **options):
        john_blog = self.create_user_and_blog('john', 'johnblog')
        bob_blog = self.create_user_and_blog('bob', 'bobblog')

        self.create_site_topbar_and_category()
        self.create_site_sidebar()

        self.create_blog_topbar_and_category(john_blog)
        self.create_blog_topbar_and_category(bob_blog)

        self.create_blog_sidebar(john_blog)
        self.create_blog_sidebar(bob_blog)

    def create_user_and_blog(self, username, blog_name):
        """创建两个用户及其对应的博客"""
        user, _ = BlogUser.objects.get_or_create(username=username)
        user.set_password('password123')
        user.email = '{0}@example.com'.format(blog_name)
        user.is_staff = True
        user.save()

        blog, _ = Blog.objects.get_or_create(name=blog_name)
        blog.user = user
        blog.save()
        return blog

    def create_site_topbar_and_category(self):
        """创建主站功能和分类顶栏"""
        github_topbar, _ = SiteTopbar.objects.get_or_create(name='github')
        github_topbar.display_type = SiteTopbar.DISPLAY_URL
        github_topbar.display_index = 1
        github_topbar.content = 'https://github.com/wangyangang'
        github_topbar.save()

        admin_topbar, _ = SiteTopbar.objects.get_or_create(name='管理')
        admin_topbar.display_type = SiteTopbar.DISPLAY_ADMIN
        admin_topbar.display_index = 2
        admin_topbar.save()

        myblog_topbar, _ = SiteTopbar.objects.get_or_create(name='我的博客')
        myblog_topbar.display_type = SiteTopbar.DISPLAY_MY_BLOG
        myblog_topbar.display_index = 3
        myblog_topbar.save()

        frontend_category_topbar, _ = SiteCategory.objects.get_or_create(name='前端')
        frontend_category_topbar.status = SiteCategory.STATUS_NORMAL
        frontend_category_topbar.is_nav = True
        frontend_category_topbar.save()

        backend_category_topbar, _ = SiteCategory.objects.get_or_create(name='后端')
        backend_category_topbar.status = SiteCategory.STATUS_NORMAL
        backend_category_topbar.is_nav = True
        backend_category_topbar.save()

        database_category_topbar, _ = SiteCategory.objects.get_or_create(name='数据库')
        database_category_topbar.status = SiteCategory.STATUS_NORMAL
        database_category_topbar.is_nav = True
        database_category_topbar.save()

        topbar_not_nav1, _ = SiteCategory.objects.get_or_create(name='非导航分类1')
        topbar_not_nav1.status = SiteCategory.STATUS_NORMAL
        topbar_not_nav1.is_nav = False
        topbar_not_nav1.save()

    def create_site_sidebar(self):
        """床架网站侧边栏"""
        welcome_sidebar, _ = SiteSidebar.objects.get_or_create(title='welcome')
        welcome_sidebar.display_type = SiteSidebar.DISPLAY_HTML
        welcome_sidebar.display_index = 2
        welcome_sidebar.content = 'this is welcome information.'
        welcome_sidebar.status = SiteSidebar.STATUS_SHOW
        welcome_sidebar.save()

        hot_article_sidebar, _ = SiteSidebar.objects.get_or_create(title='最热文章')
        hot_article_sidebar.display_type = SiteSidebar.DISPLAY_HOT
        hot_article_sidebar.display_index = 1
        hot_article_sidebar.status = SiteSidebar.STATUS_SHOW
        hot_article_sidebar.save()

    def create_blog_topbar_and_category(self, blog):
        """创建个人博客的顶部功能和分类"""
        stackoverflow_topbar, _ = TopBar.objects.get_or_create(name='django文档', blog=blog)
        stackoverflow_topbar.display_type = TopBar.DISPLAY_URL
        stackoverflow_topbar.show_type = True
        stackoverflow_topbar.display_index = 99
        stackoverflow_topbar.content = 'https://stackoverflow.com'
        stackoverflow_topbar.save()

        archive_topbar, _ = TopBar.objects.get_or_create(name='归档', blog=blog)
        archive_topbar.display_type = TopBar.DISPLAY_ARCHIVE
        archive_topbar.display_index = 999
        archive_topbar.save()

        admin_topbar, _ = TopBar.objects.get_or_create(name='管理', blog=blog)
        admin_topbar.display_type = TopBar.DISPLAY_ADMIN
        admin_topbar.display_index = 9999
        admin_topbar.save()

        site_home_topbar, _ = TopBar.objects.get_or_create(name='网站首页', blog=blog)
        site_home_topbar.display_type = TopBar.DISPLAY_HOME
        site_home_topbar.display_index = 90000
        site_home_topbar.save()

        links_topbar, _ = TopBar.objects.get_or_create(name='友链', blog=blog)
        links_topbar.display_type = TopBar.DISPLAY_LINKS
        links_topbar.display_index = 2
        links_topbar.save()

        about_topbar, _ = TopBar.objects.get_or_create(name='关于', blog=blog)
        about_topbar.display_type = TopBar.DISPLAY_ABOUT
        about_topbar.display_index = 1
        about_topbar.save()

        django_category, _ = Category.objects.get_or_create(name='Django', blog=blog)
        django_category.status = Category.STATUS_NORMAL
        django_category.is_nav = True
        django_category.save()

        flask_category, _ = Category.objects.get_or_create(name='Flask', blog=blog)
        flask_category.status = Category.STATUS_NORMAL
        flask_category.is_nav = True
        flask_category.save()

        tornado_category, _ = Category.objects.get_or_create(name='Tornado', blog=blog)
        tornado_category.status = Category.STATUS_NORMAL
        tornado_category.is_nav = True
        tornado_category.save()

    def create_blog_sidebar(self, blog):
        welcome_sidebar, _ = SideBar.objects.get_or_create(title='welcome', blog=blog)
        welcome_sidebar.display_type = SideBar.DISPLAY_HTML
        welcome_sidebar.display_index = 999
        welcome_sidebar.content = '欢迎您！'
        welcome_sidebar.status = SideBar.STATUS_SHOW
        welcome_sidebar.save()

        latest_sidebar, _ = SideBar.objects.get_or_create(title='最新文章', blog=blog)
        latest_sidebar.display_type = SideBar.DISPLAY_LATEST
        latest_sidebar.display_index = 996
        latest_sidebar.status = SideBar.STATUS_SHOW
        latest_sidebar.save()

        hot_sidebar, _ = SideBar.objects.get_or_create(title='最热文章', blog=blog)
        hot_sidebar.display_type = SideBar.DISPLAY_HOTEST
        hot_sidebar.display_index = 997
        hot_sidebar.status = SideBar.STATUS_SHOW
        hot_sidebar.save()

        comment_sidebar, _ = SideBar.objects.get_or_create(title='最新评论', blog=blog)
        comment_sidebar.display_type = SideBar.DISPLAY_COMMENT
        comment_sidebar.display_index = 998
        comment_sidebar.status = SideBar.STATUS_SHOW
        comment_sidebar.save()

