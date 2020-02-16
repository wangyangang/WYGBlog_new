from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
import os
from django.views import View
from django.views.generic import DetailView, ListView
from django.db.models import Q

from . import models
from config.models import SideBar, Link
from comment.models import Comment
from comment.forms import CommentForm


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars': SideBar.get_all()})
        context.update(models.Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = models.Post.latest_posts()
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'blog/index.html'


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


class PostDetailView(CommonViewMixin, DetailView):
    # model = models.Post
    template_name = 'blog/detail.html'
    queryset = models.Post.latest_posts()
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class LinkListView(CommonViewMixin, ListView):
    template_name = 'config/links.html'
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    context_object_name = 'links'


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
        return queryset.filter(owner_id=owner_id)


class AboutListView(IndexView):
    template_name = 'about.html'
