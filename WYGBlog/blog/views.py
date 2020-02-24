import os
from datetime import date

from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, Http404
from django.urls import reverse
from django.core.cache import cache
from django.views import View
from django.views.generic import DetailView, ListView, RedirectView
from django.db.models import Q, F
from django.shortcuts import redirect
from django.contrib.auth.models import User

from . import models
from config.models import SideBar, Link, TopBar
from comment.models import Comment
from comment.forms import CommentForm
from config.models import BlogSettings


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_name = self.kwargs.get('blog_name')  # 博客名

        context.update({'sidebars': SideBar.get_all_by_blog_name(blog_name)})  # 侧边栏
        context.update(models.Category.get_by_blog_name(blog_name))  # 分类导航
        context.update({'top_bars': TopBar.get_by_blog_name(blog_name)})  # 顶部菜单
        blog_setting = BlogSettings.get_dict_by_blog_name(blog_name)  # 用户设置
        context.update(dict(blog_setting))  # 用户配置
        context.update({'blog_name': blog_name})
        return context


class IndexView(CommonViewMixin, ListView):
    paginate_by = 8  # 在init方法里，读取网站配置里的首页文章展示条数
    context_object_name = 'posts'
    template_name = 'blog/index.html'

    def __init__(self):
        super().__init__()
        blog_settings = BlogSettings.objects.first()
        if blog_settings:
            IndexView.paginate_by = blog_settings.get_dict().get('index_post_count')

    def get_queryset_cache_key(self):
        """子类定制缓存key"""
        cache_key = "index_{page}".format(page=self.page_kwarg)
        return cache_key

    def get_queryset_data(self):
        """子类定制获取数据的方法"""
        blog_name = self.kwargs.get('blog_name', '')
        if blog_name:
            posts = models.Post.latest_posts(blog_name)
        else:
            posts = models.Post.latest_posts()
        return posts

    def get_queryset_from_cache(self, cache_key):
        value = cache.get(cache_key)
        if value:
            return value
        else:
            posts = self.get_queryset_data()
            cache.set(cache_key, posts)
            return posts

    def get_queryset(self, **kwargs):
        print(kwargs.get('blog_name', ''))
        # key = self.get_queryset_cache_key()
        # value = self.get_queryset_from_cache(key)
        posts = models.Post.latest_posts(self.kwargs.get('blog_name', None))
        return posts


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(models.Category, pk=category_id)
        context.update({'category': category})
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(models.Tag, pk=tag_id)
        context.update({"tag": tag})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class ArchiveView(IndexView):
    template_name = 'blog/archive.html'

    def __init__(self):
        super().__init__()
        blog_settings = BlogSettings.objects.first()
        if blog_settings:
            ArchiveView.paginate_by = blog_settings.get_dict().get('archive_post_count')  # 归档页面每页展示条数

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     blog_name = self.kwargs.get('blog_name')
    #     blog_settings = BlogSettings.get_dict_by_blog_name(blog_name)
    #     archive_post_count = blog_settings


class PostDetailView(CommonViewMixin, DetailView):
    template_name = 'blog/detail.html'
    # queryset = models.Post.latest_posts()
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'blog_name': self.kwargs.get('blog_name')})
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def get_queryset(self):
        blog_name = self.kwargs.get('blog_name')
        posts = models.Post.latest_posts(blog_name)
        return posts

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key, 1, 24*60*60)

        if increase_pv and increase_uv:
            models.Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            models.Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            models.Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class LinkListView(CommonViewMixin, ListView):
    template_name = 'config/links.html'
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    context_object_name = 'links'

    def get_queryset(self):
        return Link.get_all_by_blog_name(self.request.user)


class SearchView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'keyword': self.request.GET.get('keyword', '')})
        return context


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.kwargs.get('owner_id')
        return queryset.filter()


class AboutListView(IndexView):
    template_name = 'about.html'


# def blog_view(request, username):
#     if request.method == 'GET':
#         user = User.objects.filter(username=username)
#         if user:
#             return redirect('index')
#         else:
#             return HttpResponse('页面不存在')

class Redirect2HomeView(RedirectView):
    pattern_name = 'home:index'