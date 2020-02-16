from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^add_comment', views.AddCommentView.as_view(), name='add_comment')
]