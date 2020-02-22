from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User


class CommenViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.user.username
        context.update({'user_name': user_name})
        return context


class IndexView(CommenViewMixin, ListView):
    template_name = 'user/index.html'

    def get_queryset(self):
        return self.request.user.username
