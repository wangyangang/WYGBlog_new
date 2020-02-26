from django.contrib import admin
from django.contrib.auth.models import User

from .models import BlogUser


class BlogUserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(username=request.user.username)


admin.site.register(BlogUser, BlogUserAdmin)
