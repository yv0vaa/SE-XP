# 🚀 Быстрая настройка S3 за 5 минут

## Что это даёт?

Вместо сохранения файлов локально на сервере, все загружаемые файлы (домашние задания студентов) будут храниться в облаке Amazon S3.

## Шаг 1: Создайте S3 бакет

1. Зайдите на [AWS S3 Console](https://s3.console.aws.amazon.com/)
2. Нажмите **"Create bucket"**
3. Введите имя: `hw-checker-submissions` (или любое другое уникальное имя)
4. Выберите регион: `us-east-1` (или ближайший к вам)
5. Оставьте остальные настройки по умолчанию
6. Нажмите **"Create bucket"**

## Шаг 2: Получите Access Keys

1. Откройте [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Перейдите в **Users** → **Add users**
3. Имя пользователя: `hw-checker-app`
4. Отметьте ✅ **Programmatic access**
5. Нажмите **Next**, выберите **Attach existing policies directly**
6. Найдите и отметьте **AmazonS3FullAccess**
7. Нажмите **Next** → **Create user**
8. ⚠️ **СОХРАНИТЕ** Access Key ID и Secret Access Key!

## Шаг 3: Настройте проект

1. Скопируйте пример конфигурации:
```bash
cd hw_checker
cp .env.example .env
```

2. Отредактируйте `.env` файл:
```bash
USE_S3=True
AWS_ACCESS_KEY_ID=ваш_access_key_id
AWS_SECRET_ACCESS_KEY=ваш_secret_access_key
AWS_STORAGE_BUCKET_NAME=hw-checker-submissions
AWS_S3_REGION_NAME=us-east-1
```

3. Замените значения на ваши реальные данные из Шага 2.

## Шаг 4: Готово!

Запустите сервер и проверьте:
```bash
python manage.py runserver
```

Загрузите файл как студент - он автоматически сохранится в S3! ✅

## Отключение S3 (для локальной разработки)

Чтобы вернуться к локальному хранению файлов:
```bash
# В файле .env измените:
USE_S3=False
```

## 📚 Подробная документация

Полная инструкция с настройками безопасности: [S3_SETUP.md](./S3_SETUP.md)

