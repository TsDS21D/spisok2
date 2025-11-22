#!/bin/bash

echo "🚀 Deploying reactive application to production..."

# Параметры
PROJECT_DIR="/var/www/www-root/data/www/beauty-print.ru"

cd $PROJECT_DIR

# Создаем бэкап базы данных
echo "💾 Creating database backup..."
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# Обновляем код из Git
echo "📥 Pulling latest changes..."
git pull origin main

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Устанавливаем и настраиваем Redis (если еще не установлен)
if ! systemctl is-active --quiet redis-server; then
    echo "🔧 Setting up Redis..."
    sudo apt update
    sudo apt install redis-server -y
    
    # Настраиваем Redis
    sudo sed -i 's/supervised no/supervised systemd/g' /etc/redis/redis.conf
    sudo sed -i 's/bind 127.0.0.1 ::1/bind 127.0.0.1/g' /etc/redis/redis.conf
    
    # Запускаем Redis
    sudo systemctl enable redis-server
    sudo systemctl start redis-server
    echo "✅ Redis installed and configured"
fi

# Применяем миграции
echo "🗃️ Applying migrations..."
python manage.py migrate

# Собираем статические файлы
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Настраиваем службу Daphne
echo "🔧 Setting up Daphne service..."
sudo tee /etc/systemd/system/daphne_beauty_print.service > /dev/null << EOF
[Unit]
Description=Daphne ASGI server for beauty-print.ru
After=network.target redis-server.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/www-root/data/www/beauty-print.ru
Environment="PATH=/var/www/www-root/data/www/beauty-print.ru/venv/bin"
Environment="PYTHONPATH=/var/www/www-root/data/www/beauty-print.ru"
ExecStart=/var/www/www-root/data/www/beauty-print.ru/venv/bin/daphne -b 127.0.0.1 -p 8001 spisok_project.asgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable daphne_beauty_print
sudo systemctl start daphne_beauty_print

# Перезагружаем Nginx
echo "🔄 Reloading Nginx..."
sudo systemctl reload nginx

# Проверяем статусы
echo "✅ Checking services status..."
sudo systemctl status daphne_beauty_print --no-pager
sudo systemctl status redis-server --no-pager

echo "🎉 Reactive application deployed successfully!"