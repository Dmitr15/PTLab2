#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

echo "Проверка наличия товаров..."
if ! python manage.py shell -c "from shop.models import Product; exit(0 if Product.objects.exists() else 1)"; then
    echo "База пуста. Загружаем фикстуры..."
    python manage.py loaddata products.yaml
else
    echo "Товары уже есть в базе."
fi

echo "Проверка администратора..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print('Админ создан: логин admin, пароль adminpassword')
else:
    print('Админ уже существует.')
"