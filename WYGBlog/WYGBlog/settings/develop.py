from .base import *

DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db2.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.mysql',
        "NAME": 'wyg_blog',
        'HOST': '120.25.224.111',
        # 'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '456wyg',
    }
}
