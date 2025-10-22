from django.urls import path
from . import views

urlpatterns = [
    # Главная и авторизация
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Студент
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/homework/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('student/submissions/', views.my_submissions, name='my_submissions'),

    # Преподаватель
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/homework/create/', views.create_homework, name='create_homework'),
    path('teacher/homework/<int:pk>/edit/', views.edit_homework, name='edit_homework'),
    path('teacher/homework/<int:pk>/delete/', views.delete_homework, name='delete_homework'),
    path('teacher/homework/<int:pk>/submissions/', views.homework_submissions, name='homework_submissions'),
    path('teacher/submission/<int:pk>/grade/', views.grade_submission, name='grade_submission'),
    path('teacher/submissions/', views.all_submissions, name='all_submissions'),
]
