"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/22/20 - 4:27 PM
"""
from django.urls import re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    # re_path(r'^login/$', views.)
    # re_path(r'^(?P<user_name>\w+)/$', views.IndexView.as_view(), name='index'),
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]