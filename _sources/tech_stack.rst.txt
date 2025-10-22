Технологический стек
====================

Обоснование выбора технологий для проекта.

Backend: Django 5.2.7 + Python 3.9+
------------------------------------

Почему Django?
~~~~~~~~~~~~~~

✅ **Скорость разработки**
   Admin panel из коробки, ORM, встроенная аутентификация

✅ **Безопасность**
   Защита от SQL-инъекций, XSS, CSRF по умолчанию

✅ **XP-friendly**
   Идеально подходит для быстрых итераций и малых релизов

✅ **Документация**
   Отличная документация для быстрого старта

Database: SQLite
----------------

Почему SQLite?
~~~~~~~~~~~~~~

✅ **Нулевая настройка**
   Файловая БД, не требует установки сервера

✅ **Достаточно для MVP**
   Подходит для демонстрации и разработки

✅ **Легко мигрировать**
   При масштабировании легко переключиться на PostgreSQL

Frontend: Django Templates + Bootstrap 5
-----------------------------------------

Почему не SPA?
~~~~~~~~~~~~~~

✅ **Простота**
   Server-side rendering без сложной инфраструктуры

✅ **Скорость разработки**
   Не нужна сборка, API, состояние на клиенте

✅ **XP принцип**
   Самое простое решение, которое работает

Линтеры и форматтеры
--------------------

Инструменты качества кода:

.. code-block:: text

   flake8==7.1.1         # PEP 8 проверки
   black==24.10.0        # Автоформатирование
   isort==5.13.2         # Сортировка импортов
   pylint==3.3.1         # Глубокий анализ кода
   pylint-django==2.5.5  # Django-специфичные правила

Почему эти инструменты?
~~~~~~~~~~~~~~~~~~~~~~~

* Обеспечивают единый стиль кода (важно для коллективного владения)
* Автоматизируют code review (находят ошибки до ревьюера)
* Интегрируются в CI/CD

Документация: Sphinx + Google Style Docstrings
-----------------------------------------------

.. code-block:: text

   Sphinx==8.1.3                    # Генератор документации
   sphinx-rtd-theme==3.0.2          # Тема ReadTheDocs
   sphinx-autodoc-typehints==2.5.0  # Автодокументация

Почему Sphinx?
~~~~~~~~~~~~~~

✅ **Генерирует документацию из docstrings**
   DRY принцип - документация из кода

✅ **Автоматическое обновление**
   Через GitHub Actions

✅ **Профессиональный вид**
   ReadTheDocs тема

Пример docstring в Google Style
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

