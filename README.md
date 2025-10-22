# SE-XP: Homework Checker

[![Tests/Flake/Black/isort](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml)
[![Documentation Status](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml)

Проект разработан в соответствии с методологией **Extreme Programming (XP)** в рамках курса по Software Engineering.

## 📖 О проекте

Веб-приложение для управления домашними заданиями с ролями студентов и преподавателей. Система позволяет преподавателям создавать курсы и задания, а студентам - сдавать работы и получать оценки с обратной связью.

**[➡️ Описание продукта и инструкции по использованию](hw_checker/README.md)**

---

## 🎯 Extreme Programming в действии

Проект полностью следует принципам XP, что отражено в процессе разработки:

### 1. **Парное программирование (Pair Programming)**

История коммитов показывает активное участие всех членов команды:
- **Vladimir Zakharov** - базовая архитектура и функционал курсов
- **Dmitrii Deruzhinskii** - тестирование и интеграция
- **Aleksei Tokarev** - документация и CI/CD

Каждая фича разрабатывалась совместно через pull request'ы с code review.

### 2. **Непрерывная интеграция (Continuous Integration)**

С самого начала проекта был настроен CI/CD pipeline:
- **Коммит 1-2** (`f478066`, `253a260`): Инициализация проекта
- **Коммит 3** (`e68bb07`, PR #1): Добавление линтеров (flake8, black, isort, pylint)
- **Коммит 8** (`ff771d4`, PR #2): Базовые тесты
- **Коммит 11** (`fc26fbc`, PR #4): Автоматическая генерация документации

Каждый push проверяется автоматически: тесты → линтеры → документация.

### 3. **Частые релизы (Small Releases)**

Разработка велась итеративно с маленькими, осмысленными коммитами:

**Итерация 1: Инфраструктура (0-30 мин)**
```
253a260 - initial commit (Django проект)
9a185d2 - docs: Initial tech requirements (ТЗ)
e68bb07 - Add linters to CI (#1)
```

**Итерация 2: Тесты и качество кода (30-60 мин)**
```
ae35d59 - fix: fix failing test
ff771d4 - Add basic tests (#2)
29ad218 - major: add makefile for quick actions
```

**Итерация 3: Курсы и основной функционал (60-90 мин)**
```
985a22c - create possibility to add courses
6f0a09f - use black formatter
93b350b - major: add courses to tests
```

**Итерация 4: Документация и финализация (90-120 мин)**
```
3aef5d2 - docs: auto docs from pr
dcbb97b - feat: update documentation uptodate
8f0118c - feat: docs refactor
```

### 4. **Простой дизайн (Simple Design)**

Архитектура строилась по принципу YAGNI (You Aren't Gonna Need It):
- Использование стандартной Django ORM (без лишних абстракций)
- SQLite для простоты развертывания
- Bootstrap 5 через CDN (без сложных сборщиков)
- Минимальная, но достаточная функциональность (MVP)

### 5. **Рефакторинг (Refactoring)**

История показывает постоянное улучшение кода:
```
6f0f162 - fix: formatting
1f4b3a1 - fix: linter errors
c9fcd7f - fix: black and doc tests
725ff53 - fix: 3 hours instead of 4
```

### 6. **Коллективное владение кодом (Collective Code Ownership)**

Все члены команды работали в парах
- Тесты: Dmitrii, Vladimir
- Документация: Aleksei, Dmitrii
- Курсы: Vladimir, Dmitrii

### 7. **Тест-ориентированная разработка (TDD)**

Тесты были добавлены на ранней стадии (PR #2) и дополнялись с каждой новой фичей:
```python
# Тесты безопасности
- Разграничение доступа по ролям
- Изоляция данных (студент видит только свои курсы)
- Защита от несанкционированного доступа
```

---

## 🛠 Выбор технологического стека

### Backend: Django 5.2.7 + Python 3.9+

**Почему Django?**
- ✅ **Скорость разработки**: Admin panel из коробки, ORM, встроенная аутентификация
- ✅ **Безопасность**: Защита от SQL-инъекций, XSS, CSRF по умолчанию
- ✅ **XP-friendly**: Идеально подходит для быстрых итераций и малых релизов
- ✅ **Документация**: Отличная документация для быстрого старта

### Database: SQLite

**Почему SQLite?**
- ✅ Нулевая настройка (файловая БД)
- ✅ Достаточно для MVP
- ✅ Легко мигрировать на PostgreSQL при масштабировании

### Frontend: Django Templates + Bootstrap 5

**Почему не SPA?**
- ✅ **Простота**: Server-side rendering без сложной инфраструктуры
- ✅ **Скорость**: Не нужна сборка, API, состояние на клиенте
- ✅ **XP принцип**: Самое простое решение, которое работает

### Линтеры и форматтеры

```
flake8==7.1.1      # PEP 8 проверки
black==24.10.0     # Автоформатирование
isort==5.13.2      # Сортировка импортов
pylint==3.3.1      # Глубокий анализ кода
pylint-django==2.5.5  # Django-специфичные правила
```

**Почему эти инструменты?**
- Обеспечивают единый стиль кода (важно для коллективного владения)
- Автоматизируют code review (находят ошибки до ревьюера)
- Интегрируются в CI/CD

### Документация: Sphinx + Google Style Docstrings

```
Sphinx==8.1.3                    # Генератор документации
sphinx-rtd-theme==3.0.2          # Тема ReadTheDocs
sphinx-autodoc-typehints==2.5.0  # Автодокументация
```

**Почему Sphinx?**
- ✅ Генерирует документацию из docstrings (DRY принцип)
- ✅ Автоматически обновляется через GitHub Actions
- ✅ Профессиональный вид (ReadTheDocs)

---

## 📋 Требования

**[➡️ Полное техническое задание](docs/Requirenments.md)**

Проект полностью реализует требования ТЗ версии 1.1:

### Реализованные функциональные требования

#### Для студентов (100%)
- ✅ **FR-3**: Список курсов и домашних заданий
- ✅ **FR-4**: Детальный просмотр ДЗ
- ✅ **FR-5**: Отправка решения (файл)
- ✅ **FR-6**: Просмотр оценок и отзывов
- ✅ **FR-7**: Таблица с результатами

#### Для преподавателей (100%)
- ✅ **FR-8**: Управление курсами (CRUD) через веб-интерфейс
- ✅ **FR-9**: Управление домашними заданиями (CRUD)
- ✅ **FR-10**: Проверка работ и выставление оценок

#### Безопасность (100%)
- ✅ **NFR-2**: Разграничение прав по ролям
- ✅ **NFR-3**: Защита `/admin` (только администраторы)
- ✅ **NFR-4**: Защита от SQL-инъекций и XSS
- ✅ **T-SEC-1, T-SEC-2, T-SEC-3**: Все тесты безопасности пройдены

### Отклонения от ТЗ (улучшения)

**ТЗ**: Преподаватели работают через админку Django  
**Реализовано**: Преподаватели работают через отдельный веб-интерфейс (улучшение UX)

**Обоснование**: 
- Админка Django предназначена для администраторов
- Отдельный интерфейс более интуитивен и безопасен
- Следует XP принципу: "Делай самое простое, что может сработать, но для пользователя"

---

## 🚀 Быстрый старт

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
pip install -r requirements-dev.txt  # для разработки

# Перейдите в директорию проекта
cd hw_checker

# Выполните миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ в браузере.

**[➡️ Детальная инструкция по использованию](hw_checker/README.md)**

---

## 🧪 Разработка

### Структура проекта

```
SE-XP/
├── hw_checker/           # Django приложение (продукт)
│   ├── assignments/      # Основное приложение
│   │   ├── models.py    # Модели: Course, Homework, Submission
│   │   ├── views.py     # Views для студентов и преподавателей
│   │   ├── forms.py     # Формы
│   │   ├── tests.py     # Тесты
│   │   ├── decorators.py # Декораторы доступа
│   │   └── templates/   # HTML шаблоны
│   └── hw_checker/      # Настройки Django
├── docs/                # Sphinx документация
├── requirements.txt     # Зависимости продакшена
├── requirements-dev.txt # Зависимости разработки
├── Makefile            # Команды для разработки
└── .github/workflows/  # CI/CD
```

### Запуск тестов

```bash
# Все тесты
cd hw_checker
python manage.py test

# С покрытием
python manage.py test --verbosity=2

# Конкретное приложение
python manage.py test assignments
```

Текущее покрытие: **базовые тесты безопасности и функциональности**

### Линтинг и форматирование

```bash
# Автоформатирование (запускайте перед коммитом)
make format

# Или вручную:
cd hw_checker
black .
isort --profile black .

# Проверка стиля
make lint

# Или вручную:
flake8 hw_checker/
pylint hw_checker/assignments/
```

**Важно**: CI проверяет все автоматически. Pull request не будет смержен, если есть ошибки линтера.

### Сборка документации

```bash
# Локальная сборка
cd docs
make html
open _build/html/index.html  # macOS
# или
xdg-open _build/html/index.html  # Linux

# Онлайн-документация
# Автоматически публикуется на GitHub Pages при коммите в main
```

**[➡️ Онлайн-документация](https://yv0vaa.github.io/SE-XP/)**

### Makefile команды

```bash
make help       # Список всех команд
make install    # Установить все зависимости
make migrate    # Применить миграции
make run        # Запустить сервер
make test       # Запустить тесты
make lint       # Проверить код линтерами
make format     # Автоформатирование кода
make docs       # Собрать документацию
make clean      # Очистить временные файлы
```

---

## 📊 CI/CD Pipeline

### Автоматизация через GitHub Actions

#### 1. **CI Pipeline** (`.github/workflows/ci.yml`)

Запускается при:
- Push в `main`
- Pull Request

Шаги:
1. ✅ Setup Python (3.10, 3.11, 3.12) - matrix strategy
2. ✅ Установка зависимостей
3. ✅ Линтинг (flake8, black, isort, pylint)
4. ✅ Запуск тестов
5. ✅ Проверка миграций

#### 2. **Documentation Pipeline** (`.github/workflows/docs.yml`)

Запускается при:
- Push в `main`

Шаги:
1. ✅ Сборка Sphinx документации
2. ✅ Публикация на GitHub Pages
3. ✅ Автоматическое обновление онлайн-документации

### Статусы сборок

[![Tests/Flake/Black/isort](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml)
[![Documentation Status](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml)

---

## 🤝 Контрибуция

Проект следует XP практикам:

### Процесс внесения изменений

1. **Создайте ветку**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Напишите тесты** (TDD)
   - Сначала пишем failing test
   - Потом реализуем функционал
   - Проверяем, что тест проходит

3. **Напишите код**
   - Следуйте PEP 8
   - Добавьте docstrings (Google Style)
   - Простой дизайн (YAGNI)

4. **Проверьте качество**
   ```bash
   make format  # Автоформатирование
   make lint    # Проверка стиля
   make test    # Запуск тестов
   ```

5. **Создайте Pull Request**
   - Опишите изменения
   - Ссылка на issue (если есть)
   - Дождитесь code review
   - CI должен пройти успешно

### Стиль docstrings (Google Style)

```python
def create_course(title: str, description: str, teacher: User) -> Course:
    """
    Создает новый курс с указанным преподавателем.
    
    Args:
        title: Название курса.
        description: Описание курса.
        teacher: Пользователь с ролью преподавателя.
        
    Returns:
        Созданный объект Course.
        
    Raises:
        ValueError: Если teacher не является преподавателем.
        
    Examples:
        >>> teacher = User.objects.get(username='teacher1')
        >>> course = create_course('Python', 'Основы Python', teacher)
        >>> print(course.title)
        Python
    """
    if not teacher.profile.is_teacher:
        raise ValueError("User must be a teacher")
    
    course = Course.objects.create(
        title=title,
        description=description
    )
    course.teachers.add(teacher)
    return course
```

---

## 📚 Дополнительные ресурсы

- **[Техническое задание](docs/Requirenments.md)** - полное ТЗ версии 1.1
- **[Онлайн-документация](https://yv0vaa.github.io/SE-XP/)** - API reference, архитектура
- **[Описание продукта](hw_checker/README.md)** - инструкции для пользователей
- **[Быстрый старт](QUICK_START.md)** - пошаговое руководство для тестирования

---

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT - см. файл [LICENSE](LICENSE) для подробностей.

---

## 👥 Команда

- **Vladimir Zakharov** - Core functionality, courses
- **Dmitrii Deruzhinskii** - Testing, integration, CI/CD
- **Aleksei Tokarev** - Documentation, deployment