from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User, Group

from home.models import Blog
from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from baseadmin import BaseOwnerAdmin
from WYGBlog.admin_site import admin_site


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1  # 控制多几个
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'blog')
    fields = ('name', 'status', 'is_nav')
    # inlines = [PostInline]  # 控制在分类页面可以编辑文章(在同一页面编辑关联数据)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'blog')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户的分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        user_blog = Blog.objects.get(user=request.user)
        if user_blog:
            return Category.objects.filter(blog=user_blog).values_list('id', 'name')
        return None

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            ret = queryset.filter(category_id=self.value())
            return ret
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'site_category', 'status',
                    'created_time', 'blog', 'operator')
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    #list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    fieldsets = (
        ('内容', {
            'fields': (
                'title',
                'content',
            ),
        }),
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('category', 'site_category', 'status'), 'tag', 'desc',
            ),
        }),
    )

    filter_horizontal = ('tag',)

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '编辑'

    # view_on_site = False

    # 编辑文章时，tag字段只能从当前用户的tag里进行选择
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tag':
            user_blog = Blog.objects.get(user=request.user)
            kwargs['queryset'] = Tag.objects.filter(blog=user_blog)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """编辑文章时，category字段只能从当前用户的category里进行选择"""
        if db_field.name == 'category':
            user_blog = Blog.objects.get(user=request.user)
            kwargs['queryset'] = Category.objects.filter(blog=user_blog)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']


admin.site.site_header = 'WYGBlog后台管理系统'  # 后台管理主界面的h1标题
admin.site.site_title = 'WYGBlog后台管理'  # 后台管理page的title，如 "选择分类来修改 | WYGBlog后台管理"
# admin.site.index_title = 'abc'  # 后台管理主界面的副标题
# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin_site.register(User)
# admin_site.register(Group)
# admin.site.site_url = reverse('blog:index', kwargs={'blog_name': 'wyg'})
# site_url = '/wyg/'
