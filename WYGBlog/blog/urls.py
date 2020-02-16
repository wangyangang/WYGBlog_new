from django.urls import re_path, path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    re_path(r'^category/(?P<category_id>\d+)/$', views.CategoryView.as_view(), name='category'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', views.TagView.as_view(), name='tag'),
    re_path(r'^post/(?P<post_id>\d+).html/$', views.PostDetailView.as_view(), name='post'),
    re_path(r'^links/$', views.LinkListView.as_view(), name='links'),
    re_path(r'^search/$', views.SearchView.as_view(), name='search'),
    re_path(r'^author/(?P<owner_id>\d+)/$', views.AuthorView.as_view(), name='author'),
    re_path('about/', views.AboutListView.as_view(), name='about'),
]