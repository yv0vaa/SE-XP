# SE-XP

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9ce3c0f45d4741a8999ba0da89f1807a)](https://app.codacy.com/gh/yv0vaa/SE-XP?utm_source=github.com&utm_medium=referral&utm_content=yv0vaa/SE-XP&utm_campaign=Badge_Grade)
[![Tests/Flake/Black/isort](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml)
[![Documentation Status](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml)

## Система проверки домашних заданий

Веб-приложение на Django для управления домашними заданиями с ролями студентов и преподавателей.

## 📚 Документация

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue?style=flat-square&logo=github)](https://yv0vaa.github.io/SE-XP/)

Полная документация проекта автоматически генерируется из docstrings и доступна онлайн:

- **[📖 Документация на GitHub Pages](https://yv0vaa.github.io/SE-XP/)** - автоматически обновляется при каждом коммите в main

### Локальная сборка документации

Для локальной сборки документации:

```bash
# Установите зависимости
pip install -r requirements.txt

# Перейдите в директорию с документацией
cd docs

# Соберите HTML документацию
make html

# Откройте документацию в браузере
open _build/html/index.html  # macOS
# или
xdg-open _build/html/index.html  # Linux
```

### Проверка покрытия docstrings

Для проверки наличия docstrings в коде:

```bash
pip install interrogate
interrogate hw_checker/assignments/ -v
```

## 🚀 Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/yv0vaa/SE-XP.git
cd SE-XP

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Выполните миграции
cd hw_checker
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер
python manage.py runserver
```

## 🧪 Тестирование и линтинг

```bash
# Запуск тестов
cd hw_checker
python manage.py test

# Линтинг кода
flake8 hw_checker/
black --check hw_checker/
isort --check-only --profile black hw_checker/
```

## 📖 CI/CD

Проект использует GitHub Actions для автоматизации:

- **CI Pipeline** (`ci.yml`) - запускает тесты и линтинг при каждом push/PR
- **Documentation Pipeline** (`docs.yml`) - автоматически собирает и публикует документацию

### Рабочие процессы

1. **Тестирование**: При каждом push в `main` или создании PR запускаются тесты на Python 3.10, 3.11, 3.12
2. **Линтинг**: Проверка кода с помощью flake8, black, isort и pylint
3. **Документация**: Автоматическая сборка и публикация документации на GitHub Pages

## 🤝 Контрибуция

Для внесения изменений:

1. Создайте форк проекта
2. Создайте ветку для фичи (`git checkout -b feature/AmazingFeature`)
3. Добавьте docstrings ко всем новым функциям и классам
4. Убедитесь, что все тесты проходят
5. Проверьте код линтерами
6. Создайте Pull Request

### Стиль docstrings

Проект использует **Google Style** docstrings:

```python
def my_function(param1, param2):
    """
    Краткое описание функции.
    
    Более подробное описание функции, если необходимо.
    
    Args:
        param1 (str): Описание первого параметра.
        param2 (int): Описание второго параметра.
        
    Returns:
        bool: Описание возвращаемого значения.
        
    Raises:
        ValueError: Описание возможных исключений.
    """
    pass
```

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT - см. файл [LICENSE](LICENSE) для подробностей.
