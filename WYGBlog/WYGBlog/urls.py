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
from .autocomplete import CategoryAutocomplete, TagAutocomplete
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('comment/', include(('comment.urls', 'comment'), namespace='comment')),
    re_path(r'^rss|feed/', LatestPostFeed(), name='rss'),
    re_path(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    re_path(r'^category-autocomplete/$', CategoryAutocomplete.as_view(),
            name='category-autocomplete'),
    re_path(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path(r'mdeditor/', include('mdeditor.urls')),
    path('', IndexView.as_view(), name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
