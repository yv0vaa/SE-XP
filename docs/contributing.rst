Руководство для разработчиков
=============================

Спасибо за интерес к развитию проекта HW Checker!

Как начать
----------

1. Форкните репозиторий
2. Клонируйте свой форк:

   .. code-block:: bash
   
      git clone https://github.com/your-username/SE-XP.git
      cd SE-XP

3. Создайте виртуальное окружение и установите зависимости:

   .. code-block:: bash
   
      python -m venv venv
      source venv/bin/activate  # На Windows: venv\Scripts\activate
      pip install -r requirements.txt

4. Создайте ветку для ваших изменений:

   .. code-block:: bash
   
      git checkout -b feature/your-feature-name

Стандарты кодирования
---------------------

Python код
~~~~~~~~~~

* Следуйте PEP 8
* Максимальная длина строки: 100 символов
* Используйте понятные имена переменных и функций
* Добавляйте docstrings ко всем публичным методам и классам

Пример docstring:

.. code-block:: python

   def create_homework(request):
       """
       Создание нового домашнего задания.
       
       Args:
           request: HttpRequest объект
           
       Returns:
           HttpResponse с формой создания или редирект после сохранения
           
       Raises:
           ValidationError: Если данные формы невалидны
       """
       pass

Django модели
~~~~~~~~~~~~~

* Используйте ``verbose_name`` для всех полей
* Добавляйте ``Meta`` класс с ``verbose_name`` и ``verbose_name_plural``
* Определяйте ``__str__`` метод

Django представления
~~~~~~~~~~~~~~~~~~~~

* Используйте декораторы ``@login_required`` и ``@student_required``/``@teacher_required``
* Добавляйте docstrings с описанием GET и POST методов
* Используйте messages framework для уведомлений пользователей

Тестирование
------------

Перед отправкой PR убедитесь, что:

1. Все существующие тесты проходят:

   .. code-block:: bash
   
      cd hw_checker
      python manage.py test

2. Код работает локально:

   .. code-block:: bash
   
      python manage.py runserver

3. Нет ошибок в миграциях:

   .. code-block:: bash
   
      python manage.py makemigrations --check
      python manage.py migrate

Документация
------------

При добавлении новой функциональности:

1. Обновите соответствующие .rst файлы в ``docs/``
2. Добавьте docstrings к новым функциям и классам
3. Пересоберите документацию:

   .. code-block:: bash
   
      cd docs
      make html

4. Проверьте, что документация собирается без ошибок и корректно отображается

Процесс отправки изменений
--------------------------

1. Зафиксируйте изменения:

   .. code-block:: bash
   
      git add .
      git commit -m "Описание изменений"

2. Отправьте в свой форк:

   .. code-block:: bash
   
      git push origin feature/your-feature-name

3. Создайте Pull Request на GitHub

4. Опишите в PR:
   
   * Какую проблему решает
   * Какие изменения внесены
   * Как протестировать

Что следует включить в PR
--------------------------

* ✅ Описание изменений
* ✅ Тесты для новой функциональности
* ✅ Обновленную документацию
* ✅ Обновленный CHANGELOG.rst
* ✅ Docstrings для нового кода

Структура проекта
-----------------

.. code-block:: text

   SE-XP/
   ├── docs/                    # Документация Sphinx
   │   ├── api/                 # API документация
   │   ├── conf.py              # Конфигурация Sphinx
   │   └── *.rst                # Страницы документации
   ├── hw_checker/              # Django проект
   │   ├── assignments/         # Основное приложение
   │   │   ├── models.py        # Модели данных
   │   │   ├── views.py         # Представления
   │   │   ├── forms.py         # Формы
   │   │   ├── decorators.py    # Декораторы
   │   │   ├── urls.py          # URL маршруты
   │   │   └── templates/       # HTML шаблоны
   │   └── hw_checker/          # Настройки проекта
   │       └── settings.py
   └── requirements.txt         # Зависимости

Вопросы?
--------

Если у вас есть вопросы:

* Создайте Issue на GitHub
* Напишите в обсуждения (Discussions)
* Свяжитесь с мейнтейнерами проекта

Спасибо за ваш вклад! 🎉

