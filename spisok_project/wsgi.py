"""
WSGI config for spisok_project project.
"""

import os
import sys

# Добавляем путь к проекту в Python path
path = '/var/www/www-root/data/www/beauty-print.ru'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spisok_project.settings')

application = get_wsgi_application()