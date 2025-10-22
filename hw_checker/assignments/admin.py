"""
Модуль административной панели Django для приложения assignments.

Содержит конфигурацию отображения моделей в админ-панели Django.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Homework, Submission, UserProfile


class UserProfileInline(admin.StackedInline):
    """Встроенная форма профиля пользователя для админ-панели."""

    model = UserProfile
    can_delete = False
    verbose_name_plural = "Профиль"


class UserAdmin(BaseUserAdmin):
    """Расширенная админ-панель пользователя с профилем."""

    inlines = (UserProfileInline,)


# Перерегистрируем User с профилем
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    """Админка для домашних заданий"""

    list_display = ["title", "due_date", "created_at"]
    list_filter = ["created_at", "due_date"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Админка для отправок работ"""

    list_display = ["homework", "student", "submitted_at", "grade"]
    list_filter = ["submitted_at", "grade", "homework"]
    search_fields = ["student__username", "homework__title"]
    ordering = ["-submitted_at"]
    readonly_fields = ["submitted_at"]

    fieldsets = (
        ("Информация о работе", {"fields": ("homework", "student", "solution_file", "submitted_at")}),
        ("Проверка", {"fields": ("grade", "feedback")}),
    )
