from django.contrib import admin

from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser
