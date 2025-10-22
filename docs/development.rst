Руководство по разработке
=========================

Структура проекта
-----------------

.. code-block:: text

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

Команды разработки
------------------

Makefile предоставляет удобные команды для разработки:

Установка зависимостей
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make install    # Установить все зависимости

Работа с базой данных
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make migrate    # Применить миграции
   make makemigrations  # Создать новые миграции

Запуск сервера
~~~~~~~~~~~~~~

.. code-block:: bash

   make run        # Запустить сервер разработки

Тестирование
~~~~~~~~~~~~

.. code-block:: bash

   make test       # Запустить все тесты

Или вручную:

.. code-block:: bash

   cd hw_checker
   python manage.py test
   
   # С подробным выводом
   python manage.py test --verbosity=2
   
   # Конкретное приложение
   python manage.py test assignments

Текущее покрытие: **базовые тесты безопасности и функциональности**

Линтинг и форматирование
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

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

.. warning::
   CI проверяет все автоматически. Pull request не будет смержен, если есть ошибки линтера.

Сборка документации
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Локальная сборка
   cd docs
   make html
   open _build/html/index.html  # macOS
   # или
   xdg-open _build/html/index.html  # Linux
   
   # Онлайн-документация автоматически публикуется
   # на GitHub Pages при коммите в main

Очистка
~~~~~~~

.. code-block:: bash

   make clean      # Очистить временные файлы

Помощь
~~~~~~

.. code-block:: bash

   make help       # Список всех команд

Создание новых фич
------------------

1. Создайте ветку
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/amazing-feature

2. Напишите тесты (TDD)
~~~~~~~~~~~~~~~~~~~~~~~

* Сначала пишем failing test
* Потом реализуем функционал
* Проверяем, что тест проходит

3. Напишите код
~~~~~~~~~~~~~~~

* Следуйте PEP 8
* Добавьте docstrings (Google Style)
* Простой дизайн (YAGNI)

4. Проверьте качество
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make format  # Автоформатирование
   make lint    # Проверка стиля
   make test    # Запуск тестов

5. Создайте Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

* Опишите изменения
* Ссылка на issue (если есть)
* Дождитесь code review
* CI должен пройти успешно

Стандарты кодирования
---------------------

Смотрите раздел :doc:`contributing` для подробных стандартов кодирования.

Полезные команды Django
-----------------------

Создание суперпользователя
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py createsuperuser

Создание новых миграций
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py makemigrations

Запуск интерактивной оболочки
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py shell

Сборка статических файлов
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py collectstatic

Проверка настроек
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py check

