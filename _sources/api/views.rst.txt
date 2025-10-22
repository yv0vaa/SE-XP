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
   :no-index:

   Регистрация нового пользователя в системе.
   
   * **GET**: Отображает форму регистрации
   * **POST**: Обрабатывает отправку формы и создает нового пользователя

.. autofunction:: assignments.views.login_view
   :no-index:

   Вход пользователя в систему.
   
   * **GET**: Отображает форму входа
   * **POST**: Аутентифицирует пользователя

.. autofunction:: assignments.views.logout_view
   :no-index:

   Выход пользователя из системы.

Dashboard
---------

.. autofunction:: assignments.views.dashboard_view
   :no-index:

   Главная страница - перенаправляет на соответствующий dashboard в зависимости от роли пользователя.

Представления для студентов
---------------------------

.. autofunction:: assignments.views.student_dashboard
   :no-index:

   Dashboard студента с списком всех домашних заданий и статусом их выполнения.
   
   Показывает:
   
   * Все домашние задания
   * Статус сдачи каждого задания
   * Просроченные задания
   * Полученные оценки

.. autofunction:: assignments.views.course_detail
   :no-index:

   Детальная страница курса для студента.
   
   * **GET**: Показывает список домашних заданий курса и статусы их выполнения

.. autofunction:: assignments.views.homework_detail
   :no-index:

   Детальная страница конкретного домашнего задания.
   
   * **GET**: Показывает описание задания и форму отправки
   * **POST**: Обрабатывает отправку решения студентом

.. autofunction:: assignments.views.my_submissions
   :no-index:

   Список всех отправленных работ текущего студента.

.. autofunction:: assignments.views.my_grades
   :no-index:

   Таблица оценок студента по всем курсам.

Представления для преподавателей
--------------------------------

.. autofunction:: assignments.views.teacher_dashboard
   :no-index:

   Dashboard преподавателя с общей статистикой и последними работами.
   
   Показывает:
   
   * Все созданные задания
   * Последние отправленные работы
   * Количество непроверенных работ
   * Общую статистику

.. autofunction:: assignments.views.teacher_course_detail
   :no-index:

   Детальная страница курса для преподавателя.
   
   * **GET**: Отображает список домашних заданий и статистику по курсу

.. autofunction:: assignments.views.create_course
   :no-index:

   Создание нового курса.
   
   * **GET**: Отображает форму создания курса
   * **POST**: Сохраняет новый курс

.. autofunction:: assignments.views.edit_course
   :no-index:

   Редактирование существующего курса.
   
   * **GET**: Отображает форму редактирования
   * **POST**: Сохраняет изменения

.. autofunction:: assignments.views.manage_students
   :no-index:

   Управление студентами курса.
   
   * **GET**: Отображает список всех студентов с возможностью выбора
   * **POST**: Обновляет список студентов курса

.. autofunction:: assignments.views.teacher_create_homework
   :no-index:

   Создание нового домашнего задания.
   
   * **GET**: Отображает форму создания
   * **POST**: Сохраняет новое задание

.. autofunction:: assignments.views.teacher_edit_homework
   :no-index:

   Редактирование существующего домашнего задания.
   
   * **GET**: Отображает форму редактирования
   * **POST**: Сохраняет изменения

.. autofunction:: assignments.views.teacher_homework_submissions
   :no-index:

   Список всех отправленных работ по конкретному заданию.

.. autofunction:: assignments.views.teacher_grade_submission
   :no-index:

   Проверка и выставление оценки за работу студента.
   
   * **GET**: Отображает форму оценивания
   * **POST**: Сохраняет оценку и комментарий

.. autofunction:: assignments.views.teacher_all_submissions
   :no-index:

   Список всех отправленных работ с возможностью фильтрации.
   
   Поддерживает фильтры:
   
   * ``all`` - все работы
   * ``pending`` - непроверенные работы
   * ``graded`` - проверенные работы

Общие представления
-------------------

.. autofunction:: assignments.views.home_view
   :no-index:

   Главная страница для неавторизованных пользователей.

