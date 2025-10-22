from django.urls import path

from . import views

urlpatterns = [
    # Главная и авторизация
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    # Студент
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("student/course/<int:pk>/", views.course_detail, name="course_detail"),
    path("student/homework/<int:pk>/", views.homework_detail, name="homework_detail"),
    path("student/submissions/", views.my_submissions, name="my_submissions"),
    path("student/grades/", views.my_grades, name="my_grades"),
    # Преподаватель
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/course/create/", views.create_course, name="create_course"),
    path(
        "teacher/course/<int:pk>/",
        views.teacher_course_detail,
        name="teacher_course_detail",
    ),
    path("teacher/course/<int:pk>/edit/", views.edit_course, name="edit_course"),
    path(
        "teacher/course/<int:pk>/students/",
        views.manage_students,
        name="manage_students",
    ),
    path(
        "teacher/course/<int:course_pk>/homework/create/",
        views.teacher_create_homework,
        name="teacher_create_homework",
    ),
    path(
        "teacher/homework/<int:pk>/edit/",
        views.teacher_edit_homework,
        name="teacher_edit_homework",
    ),
    path(
        "teacher/homework/<int:pk>/submissions/",
        views.teacher_homework_submissions,
        name="teacher_homework_submissions",
    ),
    path(
        "teacher/submission/<int:pk>/grade/",
        views.teacher_grade_submission,
        name="teacher_grade_submission",
    ),
    path(
        "teacher/submissions/",
        views.teacher_all_submissions,
        name="teacher_all_submissions",
    ),
]
