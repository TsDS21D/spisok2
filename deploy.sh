#!/bin/bash

# Скрипт деплоя для VPS
echo "Starting deployment..."

# Активируем виртуальное окружение
source /var/www/beauty-print.ru/venv/bin/activate

# Переходим в директорию проекта
cd /var/www/beauty-print.ru

# Получаем последние изменения из Git
git pull origin main

# Устанавливаем зависимости
pip install -r requirements.txt

# Применяем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

# Перезапускаем Gunicorn
sudo systemctl restart gunicorn

# Перезагружаем Nginx
sudo systemctl reload nginx

echo "Deployment completed successfully!"