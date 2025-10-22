from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def student_required(function=None, redirect_url="/"):
    """
    Декоратор для ограничения доступа только для студентов
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, "profile") and u.profile.is_student, login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_url="/"):
    """
    Декоратор для ограничения доступа только для преподавателей
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, "profile") and u.profile.is_teacher, login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def role_required(role):
    """
    Универсальный декоратор для проверки роли
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            if not hasattr(request.user, "profile"):
                return redirect("login")

            if request.user.profile.role != role:
                return redirect("dashboard")

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
