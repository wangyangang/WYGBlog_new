from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django.contrib.admin.models import LogEntry

from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from baseadmin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1  # 控制多几个
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    # inlines = [PostInline]  # 控制在分类页面可以编辑文章(在同一页面编辑关联数据)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户的分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
        #return None

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            ret = queryset.filter(category_id=self.value())
            return ret
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'category', 'status',
                    'created_time', 'owner', 'operator')
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    #list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )
    form = PostAdminForm

    filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '编辑'

    # 编辑文章时，tag字段只能从当前用户的tag里进行选择
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tag':
            kwargs['queryset'] = Tag.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """编辑文章时，category字段只能从当前用户的category里进行选择"""
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
