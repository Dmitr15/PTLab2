#!/bin/bash
set -e

echo "Проверка наличия данных"
if ! python manage.py shell -c "from shop.models import Product; exit(0 if Product.objects.exists() else 1)"; then
    echo "База данных пуста. Загружаем фикстуры"
    python manage.py loaddata products.yaml
else
    echo "Данные уже загружены. Пропускаем загрузку."
fi

echo "Проверка наличия администратора"
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print('Суперпользователь admin создан.')
else:
    print('Суперпользователь уже существует.')
"