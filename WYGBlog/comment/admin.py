from django.contrib import admin

from .models import Comment
from blog.models import Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'website', 'email', 'status', 'created_time')
    ordering = ['-created_time']

    # 编辑文章时，tag字段只能从当前用户的tag里进行选择
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'target':
    #         kwargs['queryset'] = Post.objects.filter(owner=request.user)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

