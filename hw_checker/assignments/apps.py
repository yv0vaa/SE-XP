"""
Конфигурация приложения assignments.

Содержит настройки приложения для системы проверки домашних заданий.
"""

from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    """
    Конфигурация приложения для управления домашними заданиями.

    Attributes:
        default_auto_field: Тип автоматического поля для первичных ключей.
        name: Имя приложения.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "assignments"
