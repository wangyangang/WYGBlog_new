"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/22/20 - 4:27 PM
"""
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<user_name>\w+)/$', views.IndexView.as_view(), name='index'),
]