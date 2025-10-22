from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Homework, Submission, UserProfile, Course


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Профиль"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Перерегистрируем User с профилем
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка для курсов"""
    list_display = ['title', 'get_teachers', 'get_students_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['teachers', 'students']
    ordering = ['title']
    
    def get_teachers(self, obj):
        return ", ".join([t.get_full_name() or t.username for t in obj.teachers.all()])
    get_teachers.short_description = 'Преподаватели'
    
    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Кол-во студентов'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь - преподаватель (не суперюзер), показываем только его курсы
        if not request.user.is_superuser and request.user.is_staff:
            qs = qs.filter(teachers=request.user)
        return qs


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    """Админка для домашних заданий"""
    list_display = ['title', 'course', 'due_date', 'created_at']
    list_filter = ['course', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'course__title']
    ordering = ['-created_at']
    fields = ['course', 'title', 'description', 'due_date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь - преподаватель (не суперюзер), показываем только ДЗ его курсов
        if not request.user.is_superuser and request.user.is_staff:
            qs = qs.filter(course__teachers=request.user)
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            # Преподаватель видит только свои курсы
            if not request.user.is_superuser and request.user.is_staff:
                kwargs["queryset"] = Course.objects.filter(teachers=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_add_permission(self, request):
        # Проверяем, есть ли у преподавателя курсы
        if not request.user.is_superuser and request.user.is_staff:
            if not Course.objects.filter(teachers=request.user).exists():
                return False
        return super().has_add_permission(request)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if not request.user.is_superuser and request.user.is_staff:
            courses_count = Course.objects.filter(teachers=request.user).count()
            if courses_count == 0:
                extra_context['courses_warning'] = 'У вас нет курсов. Создайте курс перед добавлением домашнего задания.'
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Админка для отправок работ"""
    list_display = ['get_course', 'homework', 'student', 'submitted_at', 'grade']
    list_filter = ['submitted_at', 'grade', 'homework__course', 'homework']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'homework__title', 'homework__course__title']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at']
    
    fieldsets = (
        ("Информация о работе", {"fields": ("homework", "student", "solution_file", "submitted_at")}),
        ("Проверка", {"fields": ("grade", "feedback")}),
    )
    
    def get_course(self, obj):
        return obj.homework.course.title
    get_course.short_description = 'Курс'
    get_course.admin_order_field = 'homework__course__title'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь - преподаватель (не суперюзер), показываем только отправки по его курсам
        if not request.user.is_superuser and request.user.is_staff:
            qs = qs.filter(homework__course__teachers=request.user)
        return qs
