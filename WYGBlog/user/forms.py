"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/25/20 - 1:41 AM
"""
from django.contrib.auth.forms import UserCreationForm

from user.models import BlogUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = BlogUser
        fields = ('username', 'email')
