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

Course
------

.. autoclass:: assignments.models.Course
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
   
   Модель курса. Курсы содержат домашние задания и связывают преподавателей со студентами.
   
   **Поля:**
   
   * ``title`` - название курса
   * ``description`` - описание курса
   * ``teachers`` - преподаватели курса (ManyToMany с User)
   * ``students`` - студенты, записанные на курс (ManyToMany с User)
   * ``created_at`` - дата создания (автоматически)
   
   **Связи:**
   
   * ``teaching_courses`` - обратная связь от User к курсам, которые он преподает
   * ``enrolled_courses`` - обратная связь от User к курсам, на которые он записан
   * ``homeworks`` - все домашние задания этого курса

Homework
--------

.. autoclass:: assignments.models.Homework
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:
   
   Модель домашнего задания. Каждое задание принадлежит конкретному курсу.
   
   **Поля:**
   
   * ``course`` - курс, к которому относится задание (ForeignKey)
   * ``title`` - заголовок задания
   * ``description`` - описание задания
   * ``due_date`` - срок сдачи
   * ``created_at`` - дата создания (автоматически)
   
   **Связи:**
   
   * ``submissions`` - все отправленные работы по этому заданию

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

