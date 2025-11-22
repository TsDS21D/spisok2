# Инструкция по деплою на majordomo.ru

## Подготовка к деплою

1. **Настройка settings.py для продакшена:**
   - Установить DEBUG = False
   - Проверить ALLOWED_HOSTS
   - Обновить SECRET_KEY

2. **Сбор статики:**
   ```bash
   python manage.py collectstatic