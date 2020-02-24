from django.contrib import admin

from home.models import Blog

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章、分类、标签、侧边栏、友链、站点配置这些MOdel的owner字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('blog',)

    def get_queryset(self, request):
        user_blog = Blog.objects.get(user=request.user)
        if user_blog:
            return super().get_queryset(request).filter(blog=user_blog)
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        blog = request.user.blog
        obj.blog = request.user.blog
        return super().save_model(request, obj, form, change)
