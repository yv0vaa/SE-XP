#!/usr/bin/env python
"""
Скрипт для создания суперпользователя
"""
import os

import django
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_checker.settings")
django.setup()

# Данные для администратора
username = "admin"
email = "admin@example.com"
password = "admin123"

# Проверяем, существует ли уже такой пользователь
if User.objects.filter(username=username).exists():
    print(f'✅ Пользователь "{username}" уже существует')
    user = User.objects.get(username=username)
else:
    # Создаем суперпользователя
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name="Администратор",
        last_name="Системы",
    )
    print("✅ Суперпользователь создан!")
    print(f"   Логин: {username}")
    print(f"   Пароль: {password}")
    print(f"   Email: {email}")

print("\n🔐 Для входа в админ-панель:")
print("   URL: http://127.0.0.1:8000/admin/")
print(f"   Логин: {username}")
print(f"   Пароль: {password}")
