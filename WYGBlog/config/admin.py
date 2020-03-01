import os

from django.contrib import admin
from django.urls import reverse
from django.core.exceptions import ValidationError
from . import models

from baseadmin import BaseOwnerAdmin


@admin.register(models.Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time', 'blog')
    fields = ('title', 'href', 'status', 'weight')


@admin.register(models.SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'display_index', 'content', 'created_time', 'blog')
    fields = ('title', 'display_type', 'display_index', 'content')


@admin.register(models.BlogSettings)
class BlogSettingsAdmin(BaseOwnerAdmin):
    def has_add_permission(self, request):
        """一个用户只能创建一个站点配置"""
        if self.model.objects.filter(blog__name=request.user.blog.name).count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(models.TopBar)
class TopBarAdmin(BaseOwnerAdmin):
    fields = ['name', 'display_type', 'show_type', 'display_index', 'content']
    list_display = ['name', 'display_type', 'show_type', 'display_index', 'content', 'link', 'blog']

    def save_model(self, request, obj, form, change):
        if obj.display_type == models.TopBar.DISPLAY_ARCHIVE:  # 归档
            blog_name = request.user.blog.name
            obj.link = reverse('blog:archive', kwargs={'blog_name': request.user.blog.name})
        elif obj.display_type == models.TopBar.DISPLAY_HOME:  # 首页
            obj.link = reverse('home:index')
        elif obj.display_type == models.TopBar.DISPLAY_ADMIN:  # 管理
            obj.link = reverse('admin:index')
        elif obj.display_type == models.TopBar.DISPLAY_URL:  # 自定义HTML
            obj.link = obj.content  # 把用户填的content字段里的连接内容赋值给link。Template同意用obj.link调用
        elif obj.display_type == models.TopBar.DISPLAY_LINKS:
            obj.link = reverse('blog:links', kwargs={'blog_name': request.user.blog.name})
        elif obj.display_type == models.TopBar.DISPLAY_ABOUT:
            obj.link = reverse('blog:about', kwargs={'blog_name': request.user.blog.name})
        return super().save_model(request, obj, form, change)


@admin.register(models.AboutPage)
class AboutPageAdmin(BaseOwnerAdmin):
    fields = ['content']

    def has_add_permission(self, request):
        count = self.model.objects.filter(blog__name=request.user.blog.name).count()
        if count >= 1:
            return False
        return super().has_add_permission(request)
