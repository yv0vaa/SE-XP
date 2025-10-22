Формы (Forms)
=============

Модуль содержит все формы приложения для взаимодействия с пользователем.

.. automodule:: assignments.forms
   :members:
   :undoc-members:
   :show-inheritance:

RegisterForm
------------

.. autoclass:: assignments.forms.RegisterForm
   :members:
   :undoc-members:
   :show-inheritance:
   
   Форма регистрации нового пользователя.
   
   Включает поля:
   
   * Имя пользователя (username)
   * Имя (first_name)
   * Фамилия (last_name)
   * Email
   * Пароль
   * Подтверждение пароля
   * Роль (студент или преподаватель)

HomeworkForm
------------

.. autoclass:: assignments.forms.HomeworkForm
   :members:
   :undoc-members:
   :show-inheritance:
   
   Форма создания и редактирования домашнего задания.
   
   Включает поля:
   
   * Заголовок
   * Описание
   * Срок сдачи (с виджетом DateTimeInput)

SubmissionForm
--------------

.. autoclass:: assignments.forms.SubmissionForm
   :members:
   :undoc-members:
   :show-inheritance:
   
   Форма отправки решения домашнего задания студентом.
   
   Включает поля:
   
   * Файл с решением (solution_file)

GradeForm
---------

.. autoclass:: assignments.forms.GradeForm
   :members:
   :undoc-members:
   :show-inheritance:
   
   Форма выставления оценки и комментария к работе студента.
   
   Включает поля:
   
   * Оценка (grade)
   * Комментарий преподавателя (feedback)

