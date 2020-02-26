import os

from django.contrib import admin
from django.shortcuts import reverse

from .models import Category, TopBar, SideBar, BlogSettings


# @admin_site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class TopBarAdmin(admin.ModelAdmin):
    fields = ['name', 'display_type', 'show_type', 'display_index', 'content']
    list_display = ['name', 'display_type', 'show_type', 'display_index', 'content']

    def save_model(self, request, obj, form, change):
        # if obj.display_type == TopBar.DISPLAY_MY_BLOG:  # 我的博客
        #     blog_name = request.user.blog.name
        #     obj.link = reverse('blog:index', kwargs={'blog_name': request.user.blog.name})
        if obj.display_type == TopBar.DISPLAY_HOME:
            obj.link = reverse('home:index')
        elif obj.display_type == TopBar.DISPLAY_ADMIN:
            obj.link = reverse('admin-site:index')
        elif obj.display_type == TopBar.DISPLAY_URL:
            obj.link = obj.content  # 把用户填的content字段里的连接内容赋值给link。Template同意用obj.link调用
        return super().save_model(request, obj, form, change)


class SideBarAdmin(admin.ModelAdmin):
    fields = ('title', 'display_type', 'content', 'display_index', 'status')


class BlogSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


