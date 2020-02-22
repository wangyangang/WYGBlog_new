"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/21/20 - 2:15 PM
"""
from django.urls import path
from . import views

urlpatterns = [
    path('abc/', views.ABCView.as_view(), name='abc'),
]
