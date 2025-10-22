Представления (Views)
=====================

Модуль содержит все представления приложения, разделенные по функциональности.

.. automodule:: assignments.views
   :members:
   :undoc-members:
   :show-inheritance:

Авторизация
-----------

.. autofunction:: assignments.views.register_view

   Регистрация нового пользователя в системе.
   
   * **GET**: Отображает форму регистрации
   * **POST**: Обрабатывает отправку формы и создает нового пользователя

.. autofunction:: assignments.views.login_view

   Вход пользователя в систему.
   
   * **GET**: Отображает форму входа
   * **POST**: Аутентифицирует пользователя

.. autofunction:: assignments.views.logout_view

   Выход пользователя из системы.

Dashboard
---------

.. autofunction:: assignments.views.dashboard_view

   Главная страница - перенаправляет на соответствующий dashboard в зависимости от роли пользователя.

Представления для студентов
---------------------------

.. autofunction:: assignments.views.student_dashboard

   Dashboard студента с списком всех домашних заданий и статусом их выполнения.
   
   Показывает:
   
   * Все домашние задания
   * Статус сдачи каждого задания
   * Просроченные задания
   * Полученные оценки

.. autofunction:: assignments.views.homework_detail

   Детальная страница конкретного домашнего задания.
   
   * **GET**: Показывает описание задания и форму отправки
   * **POST**: Обрабатывает отправку решения студентом

.. autofunction:: assignments.views.my_submissions

   Список всех отправленных работ текущего студента.

Представления для преподавателей
--------------------------------

.. autofunction:: assignments.views.teacher_dashboard

   Dashboard преподавателя с общей статистикой и последними работами.
   
   Показывает:
   
   * Все созданные задания
   * Последние отправленные работы
   * Количество непроверенных работ
   * Общую статистику

.. autofunction:: assignments.views.create_homework

   Создание нового домашнего задания.
   
   * **GET**: Отображает форму создания
   * **POST**: Сохраняет новое задание

.. autofunction:: assignments.views.edit_homework

   Редактирование существующего домашнего задания.
   
   * **GET**: Отображает форму редактирования
   * **POST**: Сохраняет изменения

.. autofunction:: assignments.views.delete_homework

   Удаление домашнего задания.
   
   * **GET**: Показывает страницу подтверждения
   * **POST**: Удаляет задание

.. autofunction:: assignments.views.homework_submissions

   Список всех отправленных работ по конкретному заданию.

.. autofunction:: assignments.views.grade_submission

   Проверка и выставление оценки за работу студента.
   
   * **GET**: Отображает форму оценивания
   * **POST**: Сохраняет оценку и комментарий

.. autofunction:: assignments.views.all_submissions

   Список всех отправленных работ с возможностью фильтрации.
   
   Поддерживает фильтры:
   
   * ``all`` - все работы
   * ``pending`` - непроверенные работы
   * ``graded`` - проверенные работы

Общие представления
-------------------

.. autofunction:: assignments.views.home_view

   Главная страница для неавторизованных пользователей.

