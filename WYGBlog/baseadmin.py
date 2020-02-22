from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章、分类、标签、侧边栏、友链、站点配置这些MOdel的owner字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('blog',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(blog__name=request.user.username)

    def save_model(self, request, obj, form, change):
        blog = request.user.blog
        obj.blog = request.user.blog
        return super().save_model(request, obj, form, change)
