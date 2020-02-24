from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Blog
from homeconfig.models import Category as SiteCategory, SideBar, TopBar, BlogSettings
from blog.models import Post


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # blog_name = kwargs.get('blog_name')

        context.update({'sidebars': SideBar.get_all()})  # 侧边栏
        context.update(SiteCategory.get_all())  # 分类导航
        context.update({'top_bars': TopBar.get_all()})  # 顶部菜单

        blog_setting = BlogSettings.get_dict()  # 用户设置
        context.update(dict(blog_setting))  # 用户配置
        # context.update({'blog_name': blog_name})
        return context


class HomeListView(CommonViewMixin, ListView):
    paginate_by = 5
    template_name = 'home/index.html'
    context_object_name = 'posts'

    def __init__(self):
        super().__init__()
        blog_settings = BlogSettings.objects.first()
        if blog_settings:
            HomeListView.paginate_by = blog_settings.get_dict().get('index_post_count')

    def get_queryset(self):
        posts = Post.latest_posts()
        return posts


class SearchView(HomeListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class CategoryView(HomeListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(SiteCategory, pk=category_id)
        context.update({'category': category})
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(site_category_id=category_id)
