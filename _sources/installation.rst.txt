Установка
=========

Требования
----------

* Python 3.8 или выше
* pip (менеджер пакетов Python)

Пошаговая установка
--------------------

1. Клонирование репозитория
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone <repository-url>
   cd SE-XP

2. Создание виртуального окружения (рекомендуется)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m venv venv
   
   # На Linux/Mac:
   source venv/bin/activate
   
   # На Windows:
   venv\Scripts\activate

3. Установка зависимостей
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

4. Настройка базы данных
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd hw_checker
   python manage.py migrate

5. Создание суперпользователя (опционально)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py createsuperuser

6. Запуск сервера разработки
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py runserver

Теперь приложение доступно по адресу: http://127.0.0.1:8000/

Сборка документации
-------------------

Для генерации HTML-документации:

.. code-block:: bash

   cd docs
   make html

Документация будет доступна в ``docs/_build/html/index.html``

Для других форматов:

.. code-block:: bash

   make latexpdf  # PDF документация
   make epub      # EPUB книга
   make text      # Текстовая версия

