# 📦 Настройка S3-хранилища для HW Checker

## Описание

Проект настроен для работы с Amazon S3 для хранения загруженных файлов (домашние задания студентов). Вместо сохранения файлов локально на сервере, они будут загружаться в облачное хранилище S3.

## Преимущества S3

- ✅ **Масштабируемость**: Неограниченное хранилище
- ✅ **Надежность**: 99.999999999% долговечности данных
- ✅ **Безопасность**: Приватные файлы с временными подписанными URL
- ✅ **Производительность**: Быстрая загрузка и скачивание файлов
- ✅ **Экономия**: Оплата только за использованное пространство

## 📋 Предварительные требования

1. **AWS аккаунт**: Зарегистрируйтесь на [aws.amazon.com](https://aws.amazon.com)
2. **S3 бакет**: Создайте новый бакет в AWS S3
3. **IAM пользователь**: Создайте пользователя с правами доступа к S3

## 🚀 Шаг 1: Создание S3 бакета

1. Откройте [AWS S3 Console](https://s3.console.aws.amazon.com/)
2. Нажмите **"Create bucket"**
3. Заполните параметры:
   - **Bucket name**: `hw-checker-submissions` (или любое уникальное имя)
   - **AWS Region**: выберите ближайший регион (например, `us-east-1` или `eu-central-1`)
   - **Block Public Access settings**: Оставьте все галочки включенными (блокировать публичный доступ)
   - **Bucket Versioning**: Можно включить для сохранения истории версий
4. Нажмите **"Create bucket"**

## 🔑 Шаг 2: Создание IAM пользователя

1. Откройте [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Перейдите в **Users** → **Add users**
3. Заполните:
   - **User name**: `hw-checker-app`
   - **Access type**: ✅ **Programmatic access** (для получения Access Key)
4. Нажмите **Next: Permissions**
5. Выберите **Attach existing policies directly**
6. Найдите и отметьте **AmazonS3FullAccess** (или создайте кастомную политику с минимальными правами)
7. Нажмите **Next** несколько раз и затем **Create user**
8. ⚠️ **ВАЖНО**: Сохраните **Access key ID** и **Secret access key** - они больше не будут показаны!

### Пример кастомной политики (минимальные права):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::hw-checker-submissions",
        "arn:aws:s3:::hw-checker-submissions/*"
      ]
    }
  ]
}
```

## ⚙️ Шаг 3: Настройка переменных окружения

### Вариант A: Файл `.env` (рекомендуется)

1. Создайте файл `.env` в корне проекта `/Users/vovazakharov/SE-XP/hw_checker/.env`:

```bash
# S3 Configuration
USE_S3=True
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_STORAGE_BUCKET_NAME=hw-checker-submissions
AWS_S3_REGION_NAME=us-east-1
```

2. Замените значения на свои реальные данные:
   - `AWS_ACCESS_KEY_ID` - из IAM пользователя
   - `AWS_SECRET_ACCESS_KEY` - из IAM пользователя
   - `AWS_STORAGE_BUCKET_NAME` - имя вашего бакета
   - `AWS_S3_REGION_NAME` - регион бакета

3. Установите `python-dotenv` для автоматической загрузки `.env`:

```bash
pip install python-dotenv
```

4. Обновите `hw_checker/settings.py` (добавьте в начало файла):

```python
from dotenv import load_dotenv
load_dotenv()
```

### Вариант B: Экспорт переменных в терминале

```bash
export USE_S3=True
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_STORAGE_BUCKET_NAME=hw-checker-submissions
export AWS_S3_REGION_NAME=us-east-1
```

### Вариант C: Production сервер (Heroku, AWS, и т.д.)

Настройте переменные окружения через панель управления вашего хостинга.

## 🧪 Шаг 4: Тестирование

### Локальная разработка без S3:

Если вы хотите работать без S3 (локально), просто не устанавливайте `USE_S3=True`:

```bash
# Или оставьте USE_S3 пустым
export USE_S3=False
```

В этом случае файлы будут сохраняться в локальную папку `media/`.

### Тестирование S3:

1. Запустите сервер:
```bash
cd hw_checker
source ../venv/bin/activate
python manage.py runserver
```

2. Войдите как студент и загрузите файл
3. Проверьте, что файл появился в вашем S3 бакете:
   - Откройте [AWS S3 Console](https://s3.console.aws.amazon.com/)
   - Перейдите в ваш бакет
   - Вы должны увидеть загруженный файл в папке `submissions/`

4. Скачайте файл через веб-интерфейс (как преподаватель)
5. Убедитесь, что генерируется подписанный URL с временным доступом

## 🔒 Безопасность

### Что уже настроено:

- ✅ **Приватные файлы**: `AWS_DEFAULT_ACL = "private"` - файлы не доступны публично
- ✅ **Подписанные URL**: `AWS_QUERYSTRING_AUTH = True` - доступ только по временным ссылкам
- ✅ **Время жизни URL**: `AWS_QUERYSTRING_EXPIRE = 3600` - ссылки действительны 1 час
- ✅ **Уникальные имена**: `AWS_S3_FILE_OVERWRITE = False` - файлы не перезаписываются

### Рекомендации:

1. **НЕ коммитьте** `.env` файл в git (он уже в `.gitignore`)
2. **Используйте разные бакеты** для dev/staging/production
3. **Включите версионирование** в S3 для восстановления файлов
4. **Настройте S3 Lifecycle Rules** для автоматического удаления старых файлов
5. **Мониторьте расходы** через AWS Cost Explorer

## 💰 Стоимость

### Примерные расчеты (регион US East):

- **Хранение**: $0.023 за GB в месяц
- **Запросы GET**: $0.0004 за 1000 запросов
- **Запросы PUT**: $0.005 за 1000 запросов
- **Передача данных**: Первые 100 GB/месяц бесплатно

**Пример**: 1000 студентов, 10 файлов по 5 MB каждый:
- Хранение: 50 GB × $0.023 = **$1.15/месяц**
- Запросы: ~30,000 GET + 10,000 PUT ≈ **$0.06/месяц**
- **Итого: ~$1.21/месяц**

### Бесплатный tier для новых аккаунтов (12 месяцев):

- 5 GB хранения
- 20,000 GET запросов
- 2,000 PUT запросов
- 100 GB исходящего трафика

## 🛠 Troubleshooting

### Ошибка: "Access Denied"

**Решение**: Проверьте права IAM пользователя и настройки бакета.

### Ошибка: "The bucket does not exist"

**Решение**: Проверьте имя бакета в переменных окружения.

### Ошибка: "Invalid Access Key"

**Решение**: Проверьте `AWS_ACCESS_KEY_ID` и `AWS_SECRET_ACCESS_KEY`.

### Файлы не загружаются

**Решение**: 
1. Проверьте, что `USE_S3=True`
2. Проверьте логи Django: `python manage.py runserver`
3. Проверьте права доступа IAM пользователя

### Медленная загрузка

**Решение**: Выберите регион S3 ближе к вашему местоположению.

## 🔄 Миграция существующих файлов

Если у вас уже есть файлы в локальной папке `media/`, выполните:

```bash
# Установите AWS CLI
pip install awscli

# Настройте AWS CLI
aws configure

# Скопируйте файлы в S3
aws s3 sync media/ s3://hw-checker-submissions/
```

## 📚 Дополнительные ресурсы

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [django-storages Documentation](https://django-storages.readthedocs.io/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## ✅ Готово!

Теперь ваш проект использует S3 для хранения файлов! 🎉

Для отключения S3 и возврата к локальному хранению:
```bash
export USE_S3=False
# или удалите переменную USE_S3 из .env
```

