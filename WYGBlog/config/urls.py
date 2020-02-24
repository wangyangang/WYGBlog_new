"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/23/20 - 2:15 PM
"""
from django.urls import path
from . import views

urlpatterns = [
    path('abc', views.IndexView.as_view(), name='index'),
]