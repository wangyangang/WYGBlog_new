"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/21/20 - 10:57 PM
"""
from django.contrib.admin import AdminSite
from django.shortcuts import reverse

from home.models import Blog
from home.admin import BlogAdmin
from homeconfig.models import Category, TopBar, SideBar, BlogSettings
from homeconfig.admin import CategoryAdmin, TopBarAdmin, SideBarAdmin, BlogSettingsAdmin


class WYGBlogAdminSite(AdminSite):
    site_title = 'WYGBlog site admin'
    site_header = 'WYGBlog administrator'

    def __init__(self, name='admin-site'):
        super().__init__(name)

    def has_permission(self, request):
        return request.user.is_superuser  # 管理员才可以访问


admin_site = WYGBlogAdminSite(name='admin-site')
# admin_site.register(Blog, BlogAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(TopBar, TopBarAdmin)
admin_site.register(SideBar, SideBarAdmin)
admin_site.register(BlogSettings, BlogSettingsAdmin)
# admin_site.site_url = reverse('blog:index', kwargs={'blog_name': 'wyg'})
