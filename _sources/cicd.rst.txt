CI/CD Pipeline
==============

Автоматизация через GitHub Actions
-----------------------------------

CI Pipeline
~~~~~~~~~~~

**Файл**: ``.github/workflows/ci.yml``

**Запускается при**:

* Push в ``main``
* Pull Request

**Шаги**:

1. ✅ Setup Python (3.10, 3.11, 3.12) - matrix strategy
2. ✅ Установка зависимостей
3. ✅ Линтинг (flake8, black, isort, pylint)
4. ✅ Запуск тестов
5. ✅ Проверка миграций

**Пример конфигурации**:

.. code-block:: yaml

   name: Tests/Flake/Black/isort
   
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: [3.10, 3.11, 3.12]
       
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: ${{ matrix.python-version }}
         - name: Install dependencies
           run: |
             pip install -r requirements.txt
             pip install -r requirements-dev.txt
         - name: Run linters
           run: |
             flake8 hw_checker/
             black --check hw_checker/
             isort --check hw_checker/
             pylint hw_checker/assignments/
         - name: Run tests
           run: |
             cd hw_checker
             python manage.py test

Documentation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~

**Файл**: ``.github/workflows/docs.yml``

**Запускается при**:

* Push в ``main``

**Шаги**:

1. ✅ Сборка Sphinx документации
2. ✅ Публикация на GitHub Pages
3. ✅ Автоматическое обновление онлайн-документации

**Результат**: Документация доступна онлайн на https://yv0vaa.github.io/SE-XP/

Статусы сборок
--------------

Бейджи в README показывают текущее состояние:

.. image:: https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/yv0vaa/SE-XP/actions/workflows/ci.yml
   :alt: Tests/Flake/Black/isort

.. image:: https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml/badge.svg?branch=main
   :target: https://github.com/yv0vaa/SE-XP/actions/workflows/docs.yml
   :alt: Documentation Status

Локальная проверка перед push
------------------------------

Используйте Makefile для локальной проверки:

Форматирование кода
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make format

Или вручную:

.. code-block:: bash

   cd hw_checker
   black .
   isort --profile black .

Проверка стиля
~~~~~~~~~~~~~~

.. code-block:: bash

   make lint

Или вручную:

.. code-block:: bash

   flake8 hw_checker/
   pylint hw_checker/assignments/

Запуск тестов
~~~~~~~~~~~~~

.. code-block:: bash

   make test

Или вручную:

.. code-block:: bash

   cd hw_checker
   python manage.py test

.. warning::
   Pull request не будет смержен, если есть ошибки линтера или падающие тесты!

