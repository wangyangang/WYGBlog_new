from django.contrib import admin
from django.contrib.auth.models import User

from .models import BlogUser


admin.site.register(BlogUser)
# admin.site.unregister(User)
