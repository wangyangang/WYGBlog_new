"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/21/20 - 2:05 PM
"""

from django.urls import path

from . import views

from . import views
urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('category/<category_id>/', views.CategoryView.as_view(), name='category'),
]