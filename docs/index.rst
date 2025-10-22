.. HW Checker documentation master file

Документация проекта HW Checker
================================

Добро пожаловать в документацию системы проверки домашних заданий!

HW Checker - это веб-приложение на Django для управления домашними заданиями,
их сдачи студентами и проверки преподавателями.

Содержание
----------

.. toctree::
   :maxdepth: 2
   :caption: Общая информация:

   overview
   installation
   usage

.. toctree::
   :maxdepth: 2
   :caption: API Документация:

   api/models
   api/views
   api/forms
   api/decorators

.. toctree::
   :maxdepth: 2
   :caption: Дополнительно:

   changelog
   contributing


Быстрый старт
=============

Установка
---------

.. code-block:: bash

   git clone <repository-url>
   cd SE-XP
   pip install -r requirements.txt
   cd hw_checker
   python manage.py migrate
   python manage.py runserver

Использование
-------------

1. Зарегистрируйтесь как студент или преподаватель
2. Преподаватель создает домашние задания
3. Студенты отправляют решения
4. Преподаватель проверяет и выставляет оценки


Индексы и таблицы
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

