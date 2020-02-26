from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponse

from user.models import BlogUser
from user.forms import RegisterForm


class CommenViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.user.username
        context.update({'user_name': user_name})
        return context


class IndexView(CommenViewMixin, LoginRequiredMixin, ListView):
    template_name = 'user/index.html'

    def get_queryset(self):
        return self.request.user.username


class IndexView2(View):
    def get(self, request):
        return render(request, 'accounts/profile.html')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user:index')
        form = RegisterForm()
        next_url = request.GET.get('next', '/')
        return render(request, 'user/register.html', {'form': form, 'next': next_url})

    def post(self, request):
        next_url = request.POST.get('next', '/')
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
        else:
            return render(request, 'user/register.html', {'form': form, 'next': next_url})


class SettingsView(View):
    def get(self, request):
        return render(request, 'user/settings.html')

    def post(self, request):
        pass


class AccountSettingsView(View):
    def post(self, request):
        return HttpResponse(request.POST.get('username'))
