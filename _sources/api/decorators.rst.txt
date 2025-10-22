Декораторы (Decorators)
=======================

Модуль содержит декораторы для контроля доступа на основе ролей пользователей.

.. automodule:: assignments.decorators
   :members:
   :undoc-members:
   :show-inheritance:

student_required
----------------

.. autofunction:: assignments.decorators.student_required
   :no-index:

   Декоратор для проверки, что текущий пользователь является студентом.
   
   **Использование:**
   
   .. code-block:: python
   
      @login_required
      @student_required
      def student_only_view(request):
          # Код доступен только студентам
          pass
   
   **Поведение:**
   
   * Если пользователь не авторизован - перенаправление на страницу входа
   * Если пользователь не студент - возвращается HttpResponseForbidden (403)

teacher_required
----------------

.. autofunction:: assignments.decorators.teacher_required
   :no-index:

   Декоратор для проверки, что текущий пользователь является преподавателем.
   
   **Использование:**
   
   .. code-block:: python
   
      @login_required
      @teacher_required
      def teacher_only_view(request):
          # Код доступен только преподавателям
          pass
   
   **Поведение:**
   
   * Если пользователь не авторизован - перенаправление на страницу входа
   * Если пользователь не преподаватель - возвращается HttpResponseForbidden (403)

Примеры использования
~~~~~~~~~~~~~~~~~~~~~~

Представление только для студентов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.contrib.auth.decorators import login_required
   from .decorators import student_required
   
   @login_required
   @student_required
   def homework_detail(request, pk):
       homework = get_object_or_404(Homework, pk=pk)
       return render(request, 'homework_detail.html', {'homework': homework})

Представление только для преподавателей
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.contrib.auth.decorators import login_required
   from .decorators import teacher_required
   
   @login_required
   @teacher_required
   def create_homework(request):
       if request.method == 'POST':
           form = HomeworkForm(request.POST)
           if form.is_valid():
               form.save()
       return render(request, 'create_homework.html')

