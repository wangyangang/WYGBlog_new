"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/25/20 - 3:14 PM
"""
from .models import BlogUser


class EmailBackend:
    def authenticate(self, request, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = BlogUser.objects.get(email=email)
        except BlogUser.DoesNotExist as e:
            print(e)
        else:
            if user.check_password(credentials['password']):
                return user

    def get_user(self, user_id):
        try:
            return BlogUser.objects.get(pk=user_id)
        except BlogUser.DoesNotExist:
            return None