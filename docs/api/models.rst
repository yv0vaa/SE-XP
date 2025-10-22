Модели (Models)
===============

Модуль содержит Django модели для управления пользователями, домашними заданиями и отправками работ.

.. automodule:: assignments.models
   :members:
   :undoc-members:
   :show-inheritance:

UserProfile
-----------

.. autoclass:: assignments.models.UserProfile
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
   
   Модель профиля пользователя, содержащая информацию о роли (студент или преподаватель).
   
   **Поля:**
   
   * ``user`` - связь с моделью User (один к одному)
   * ``role`` - роль пользователя ('student' или 'teacher')
   
   **Свойства:**
   
   * ``is_student`` - проверка, является ли пользователь студентом
   * ``is_teacher`` - проверка, является ли пользователь преподавателем

Homework
--------

.. autoclass:: assignments.models.Homework
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
   
   Модель домашнего задания.
   
   **Поля:**
   
   * ``title`` - заголовок задания
   * ``description`` - описание задания
   * ``due_date`` - срок сдачи
   * ``created_at`` - дата создания (автоматически)

Submission
----------

.. autoclass:: assignments.models.Submission
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
   
   Модель отправленной работы студента.
   
   **Поля:**
   
   * ``homework`` - связь с домашним заданием
   * ``student`` - связь с пользователем (студентом)
   * ``solution_file`` - загруженный файл с решением
   * ``submitted_at`` - дата и время отправки
   * ``grade`` - оценка (опционально)
   * ``feedback`` - отзыв преподавателя (опционально)
   
   **Ограничения:**
   
   * Уникальная пара (homework, student) - студент может отправить только одну работу по каждому заданию

Сигналы
-------

.. autofunction:: assignments.models.create_user_profile
   :no-index:

   Автоматически создает профиль пользователя при создании нового User.

.. autofunction:: assignments.models.save_user_profile
   :no-index:

   Автоматически сохраняет профиль пользователя при сохранении User.

