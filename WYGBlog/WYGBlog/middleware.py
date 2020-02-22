"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/21/20 - 12:26 AM
"""

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from home.models import Blog


class Username2UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        blog_name = view_args[1].get('blog_name', "")
        if blog_name:
            blog = Blog.objects.filter(name=blog_name)
            if not blog:
                return HttpResponse('not found')

        return None

