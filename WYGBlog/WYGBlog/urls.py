"""WYGBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps import views as sitemap_views

from blog.views import IndexView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from django.conf.urls.static import static
from django.conf import settings

from home.views import HomeListView
from WYGBlog.admin_site import admin_site


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('admin-site/', admin_site.urls, name='admin-site'),

    # path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('comment/', include(('comment.urls', 'comment'), namespace='comment')),
    path('rss|feed/', LatestPostFeed(), name='rss'),
    path('sitemap\.xml/', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('mdeditor/', include('mdeditor.urls')),

    path('', include(('home.urls', 'home'), namespace='home')),  # 博客园首页
    path('config', include(('config.urls', 'config'), namespace='config')),
    path('homeconfig/', include(('homeconfig.urls', 'homeconfig'), namespace='homeconfig')),
    # re_path(r'^(?P<blog_name>\w+)/$', IndexView.as_view(), name='blog'),  # 个人博客页
    re_path(r'^(?P<blog_name>\w+)/', include(('blog.urls', 'blog'), namespace='blog')),  # 个人博客页
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
