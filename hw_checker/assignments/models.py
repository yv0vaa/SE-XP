from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Профиль пользователя с ролью"""

    ROLE_CHOICES = [
        ("student", "Студент"),
        ("teacher", "Преподаватель"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student", verbose_name="Роль")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def is_student(self):
        return self.role == "student"

    @property
    def is_teacher(self):
        return self.role == "teacher"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаем профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при сохранении пользователя"""
    if hasattr(instance, "profile"):
        instance.profile.save()


class Homework(models.Model):
    """Модель домашнего задания"""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    due_date = models.DateTimeField(verbose_name="Срок сдачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Submission(models.Model):
    """Модель отправки работы студентом"""

    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="submissions", verbose_name="Домашнее задание"
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", verbose_name="Студент")
    solution_file = models.FileField(upload_to="submissions/", verbose_name="Файл с решением")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")
    feedback = models.TextField(blank=True, verbose_name="Отзыв преподавателя")

    class Meta:
        verbose_name = "Отправка работы"
        verbose_name_plural = "Отправки работ"
        ordering = ["-submitted_at"]
        unique_together = ["homework", "student"]

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"
