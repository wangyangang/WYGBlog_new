from django.urls import re_path, path, include
from django.views.generic import TemplateView
from . import views

# from blog.apis import post_list, PostList, 
from blog.apis import PostViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
# 文章的列表接口和详情接口
router.register(r'post', PostViewSet, basename='api-post')
# 分类的列表接口和详情接口
router.register('category', CategoryViewSet, basename='api-category')

urlpatterns = [
    re_path(r'^category/(?P<category_id>\d+)/$', views.CategoryView.as_view(), name='category'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', views.TagView.as_view(), name='tag'),
    re_path(r'^post/(?P<post_id>\d+).html/$', views.PostDetailView.as_view(), name='post'),
    re_path(r'^links/$', views.LinkListView.as_view(), name='links'),
    re_path(r'^search/$', views.SearchView.as_view(), name='search'),
    re_path(r'^author/(?P<owner_id>\d+)/$', views.AuthorView.as_view(), name='author'),
    re_path('about/', views.AboutListView.as_view(), name='about'),

    # rest_framework
    #re_path(r'^api/post/$', post_list, name='post-list'),
    # re_path(r'^api/post/', PostList.as_view(), name='post-list'),

    # 这样定义了之后就有了两个只读的接口，
    # /api/post/
    # /api/post/<post_id>/
    re_path(r'^api/', include((router.urls, 'api'), namespace='api')),
    # 配置接口文档  !!!!!!!!!!!!!有问题，访问/blog/api/docs/ 报错！
    re_path(r'^api/docs/', include_docs_urls(title='WYGBlog apis')),
]