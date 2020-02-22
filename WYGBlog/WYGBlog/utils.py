"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   2/20/20 - 12:20 PM
"""

from django.core.cache import cache


def get_blog_setting():
    value = cache.get('get_blog_setting')
    if value:
        return value
    else:
        from config.models import BlogSettings
        if not BlogSettings.objects.exists():
            setting = BlogSettings()
            setting.sitename = 'DjangoBlog'
            setting.save()
        value = BlogSettings.objects.first()
        cache.set('get_blog_setting', value)
        return value


def is_login():
    pass
