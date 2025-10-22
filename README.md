# SE-XP: Homework Checker

[![Tests/Flake/Black/isort](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c59fa8ac6324456bb3db35cf35055c2c)](https://app.codacy.com/gh/yv0vaa/SE-XP/dashboard)
[![Codacy Coverage](https://app.codacy.com/project/badge/Coverage/c59fa8ac6324456bb3db35cf35055c2c)](https://app.codacy.com/gh/yv0vaa/SE-XP/dashboard)
[![Documentation Status](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml)

Веб-приложение для управления домашними заданиями, разработанное по методологии **Extreme Programming (XP)** в рамках курса Software Engineering.

---

## 📖 О проекте

Система позволяет преподавателям создавать курсы и задания, а студентам — сдавать работы и получать оценки с обратной связью.

**[➡️ Описание продукта для пользователей](hw_checker/README.md)**  
**[📚 Полная документация](https://yv0vaa.github.io/SE-XP/)**

---

## 🎯 Extreme Programming

Проект полностью следует принципам XP:

- ✅ **Парное программирование** - вся разработка в парах
- ✅ **Непрерывная интеграция** - автоматическое тестирование и деплой
- ✅ **Частые релизы** - итеративная разработка с малыми коммитами
- ✅ **Простой дизайн** - архитектура по принципу YAGNI
- ✅ **Рефакторинг** - постоянное улучшение кода
- ✅ **Коллективное владение** - активное участие всей команды
- ✅ **TDD** - тесты с начала разработки

**[➡️ Подробнее о применении XP](https://yv0vaa.github.io/SE-XP/xp_practices.html)**

---

## 🛠 Технологии

- **Backend**: Django 5.2.7 + Python 3.9+
- **Database**: SQLite
- **Frontend**: Django Templates + Bootstrap 5
- **CI/CD**: GitHub Actions (линтеры, тесты, автодокументация)
- **Docs**: Sphinx + ReadTheDocs

**[➡️ Обоснование выбора технологий](https://yv0vaa.github.io/SE-XP/tech_stack.html)**

---

## 🚀 Быстрый старт

```bash
# Клонируйте репозиторий
git clone https://github.com/yv0vaa/SE-XP.git
cd SE-XP

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Выполните миграции и запустите сервер
cd hw_checker
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ в браузере.

**[➡️ Пошаговая инструкция](https://yv0vaa.github.io/SE-XP/installation.html)**  
**[➡️ Инструкция для тестирования](QUICK_START.md)**

---

## 📋 Требования

Проект полностью реализует требования ТЗ версии 1.1:

### Реализованные функциональные требования

#### Для студентов (100%)
- ✅ Список курсов и домашних заданий
- ✅ Детальный просмотр ДЗ
- ✅ Отправка решения (файл)
- ✅ Просмотр оценок и отзывов
- ✅ Таблица с результатами

#### Для преподавателей (100%)
- ✅ Управление курсами (CRUD) через веб-интерфейс
- ✅ Управление домашними заданиями (CRUD)
- ✅ Проверка работ и выставление оценок

#### Безопасность (100%)
- ✅ Разграничение прав по ролям
- ✅ Защита `/admin` (только администраторы)
- ✅ Защита от SQL-инъекций и XSS
- ✅ Все тесты безопасности пройдены

**[➡️ Полное техническое задание](https://yv0vaa.github.io/SE-XP/Requirements.html)**  
**[➡️ Описание функционала](https://yv0vaa.github.io/SE-XP/features.html)**

---

## 🧪 Разработка

### Makefile команды

```bash
make help       # Список всех команд
make install    # Установить зависимости
make run        # Запустить сервер
make test       # Запустить тесты
make lint       # Проверить код линтерами
make format     # Автоформатирование кода
make docs       # Собрать документацию
```

### Структура проекта

```
SE-XP/
├── hw_checker/           # Django приложение
│   ├── assignments/      # Основное приложение
│   │   ├── models.py    # Модели: Course, Homework, Submission
│   │   ├── views.py     # Views для студентов и преподавателей
│   │   ├── forms.py     # Формы
│   │   ├── tests.py     # Тесты
│   │   └── templates/   # HTML шаблоны
│   └── hw_checker/      # Настройки Django
├── docs/                # Sphinx документация
└── .github/workflows/  # CI/CD
```

**[➡️ Руководство по разработке](https://yv0vaa.github.io/SE-XP/development.html)**  
**[➡️ Как контрибьютить](https://yv0vaa.github.io/SE-XP/contributing.html)**

---

## 📊 CI/CD Pipeline

### Автоматизация через GitHub Actions

**CI Pipeline** - запускается при каждом push и PR:
1. ✅ Тестирование на Python 3.10, 3.11, 3.12
2. ✅ Review - Codacy
3. ✅ Линтинг (flake8, black, isort, pylint)
4. ✅ Запуск тестов
5. ✅ Проверка миграций

**Documentation Pipeline** - автоматическая публикация документации на GitHub Pages

**[➡️ Подробнее о CI/CD](https://yv0vaa.github.io/SE-XP/cicd.html)**

---

## 🤝 Контрибуция

Мы следуем XP практикам:

1. **Создайте ветку** для вашей фичи
2. **Напишите тесты** (TDD подход)
3. **Напишите код** с docstrings (Google Style)
4. **Проверьте качество**: `make format && make lint && make test`
5. **Создайте Pull Request** с описанием изменений

**[➡️ Руководство для разработчиков](https://yv0vaa.github.io/SE-XP/contributing.html)**

---

## 📚 Документация

- 📖 **[Онлайн-документация](https://yv0vaa.github.io/SE-XP/)** - полная документация на GitHub Pages
- 📘 **[Описание продукта](hw_checker/README.md)** - руководство для пользователей
- 📋 **[Техническое задание](https://yv0vaa.github.io/SE-XP/Requirements.html)** - ТЗ версии 1.1
- 🚀 **[Быстрый старт](QUICK_START.md)** - пошаговое руководство

### Разделы документации

- [Обзор проекта](https://yv0vaa.github.io/SE-XP/overview.html)
- [Установка](https://yv0vaa.github.io/SE-XP/installation.html)
- [Руководство пользователя](https://yv0vaa.github.io/SE-XP/usage.html)
- [Функциональность](https://yv0vaa.github.io/SE-XP/features.html)
- [FAQ](https://yv0vaa.github.io/SE-XP/faq.html)
- [XP практики](https://yv0vaa.github.io/SE-XP/xp_practices.html)
- [Технологический стек](https://yv0vaa.github.io/SE-XP/tech_stack.html)
- [Руководство по разработке](https://yv0vaa.github.io/SE-XP/development.html)
- [CI/CD](https://yv0vaa.github.io/SE-XP/cicd.html)
- [API Reference](https://yv0vaa.github.io/SE-XP/api/models.html)

---

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT - см. файл [LICENSE](LICENSE) для подробностей.

---

## 👥 Команда

- **Vladimir Zakharov** - Core functionality, courses
- **Dmitrii Deruzhinskii** - Testing, integration, CI/CD
- **Aleksei Tokarev** - Documentation, deployment

---

**Homework Checker** - разработан с применением методологии Extreme Programming 
