.. HW Checker documentation master file

Документация проекта HW Checker
================================

Добро пожаловать в документацию системы проверки домашних заданий!

HW Checker - это веб-приложение на Django для управления домашними заданиями,
организованными по курсам. Преподаватели создают курсы, записывают на них студентов
и создают домашние задания. Студенты сдают работы, а преподаватели проверяют их
и выставляют оценки.

Содержание
----------

.. toctree::
   :maxdepth: 2
   :caption: Общая информация:

   overview
   installation
   usage
   features
   faq

.. toctree::
   :maxdepth: 2
   :caption: Разработка проекта:

   xp_practices
   tech_stack
   development
   cicd
   contributing

.. toctree::
   :maxdepth: 2
   :caption: Требования:

   Requirements

.. toctree::
   :maxdepth: 2
   :caption: API Документация:

   api/models
   api/views
   api/forms
   api/decorators

.. toctree::
   :maxdepth: 2
   :caption: История изменений:

   changelog


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
2. Преподаватель создает курс
3. Преподаватель записывает студентов на курс
4. Преподаватель создает домашние задания в рамках курса
5. Студенты видят свои курсы и задания
6. Студенты отправляют решения (файлы)
7. Преподаватель проверяет работы и выставляет оценки
8. Студенты видят оценки и отзывы в таблице оценок


Индексы и таблицы
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

