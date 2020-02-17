# from rest_framework import generics 
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .models import Post
# from .serializers import PostSerializer


# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializers = PostSerializer(posts, many=True)
#     return Response(post_serializers.data)


# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer

from rest_framework import viewsets, serializers, pagination
from rest_framework.permissions import IsAdminUser

from .models import Post, Category
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer

# 如果想获取某个分类下的文章，可以有两种方法。
# 1.在postviewset里重写filter_queryset 方法，根据category参数，获取该category下的posts、
# 2.在categoryDetailSerializer里增加posts字段显示。

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """这里重写获取文章详情页的接口,达到不同接口使用不同serializer的目的"""
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """通过重写这个方法，可以根据URL(例如:/blog/api/post/?category=3)上的category参数获取该category下的文章"""
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    