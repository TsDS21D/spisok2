"""
WSGI config for spisok_project project.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Добавляем путь к проекту в Python path
path = '/var/www/beauty-print.ru'  # Этот путь укажите реальный путь на VPS
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spisok_project.settings')

application = get_wsgi_application()