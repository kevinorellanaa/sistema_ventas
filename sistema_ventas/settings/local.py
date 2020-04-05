from .base import *
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ventasdb',
        'USER': 'root',
        'PASSWORD': 'kingsman',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
