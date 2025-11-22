import os
import sys

# Настройка пути
INTERP = "/var/www/www-root/data/www/beauty-print.ru/venv/bin/python"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from spisok_project.wsgi import application