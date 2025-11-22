"""
Production settings for beauty-print.ru
"""

from .settings import *
import os

# Безопасность
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key-change-this')
DEBUG = False
ALLOWED_HOSTS = ['beauty-print.ru', 'www.beauty-print.ru', '178.250.242.96']

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_ROOT = '/var/www/www-root/data/www/beauty-print.ru/static'
MEDIA_ROOT = '/var/www/www-root/data/www/beauty-print.ru/media'

# Channel layers для продакшена (используем Redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}