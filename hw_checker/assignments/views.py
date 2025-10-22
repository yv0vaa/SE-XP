"""
Представления (views) для системы проверки домашних заданий.

Содержит все представления для:
- Авторизации и регистрации пользователей
- Dashboard студента и преподавателя
- Управления домашними заданиями
- Отправки и проверки работ
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponseForbidden

from .decorators import student_required, teacher_required
from .forms import GradeForm, HomeworkForm, RegisterForm, SubmissionForm
from .models import Homework, Submission, UserProfile, Course

# ============= Авторизация =============


def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.first_name}!")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "assignments/register.html", {"form": form})


def login_view(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.first_name}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, "assignments/login.html")


@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, "Вы вышли из системы")
    return redirect("login")


# ============= Dashboard =============


@login_required
def dashboard_view(request):
    """Главная страница - перенаправление в зависимости от роли"""
    if request.user.profile.is_student:
        return redirect("student_dashboard")
    elif request.user.profile.is_teacher:
        return redirect("teacher_dashboard")
    else:
        return redirect("login")


# ============= Студент =============


@login_required
@student_required
def student_dashboard(request):
    """Dashboard студента - список курсов"""
    courses = request.user.enrolled_courses.all()
    
    # Статистика по всем курсам
    all_homeworks = Homework.objects.filter(course__in=courses)
    my_submissions = Submission.objects.filter(student=request.user)
    
    context = {
        'courses': courses,
        'total_courses': courses.count(),
        'total_homeworks': all_homeworks.count(),
        'submitted_count': my_submissions.count(),
        'graded_count': my_submissions.filter(grade__isnull=False).count(),
    }
    
    return render(request, 'assignments/student_dashboard.html', context)


@login_required
@student_required
def course_detail(request, pk):
    """Детальная страница курса для студента"""
    course = get_object_or_404(Course, pk=pk)
    
    # Проверка доступа - студент должен быть записан на курс
    if request.user not in course.students.all():
        messages.error(request, 'У вас нет доступа к этому курсу')
        return redirect('student_dashboard')
    
    homeworks = course.homeworks.all().order_by('-created_at')
    my_submissions = Submission.objects.filter(student=request.user, homework__course=course)
    
    # Добавляем информацию о том, сдал ли студент каждое ДЗ
    homework_status = []
    for hw in homeworks:
        submission = my_submissions.filter(homework=hw).first()
        homework_status.append(
            {
                "homework": hw,
                "submission": submission,
                "is_overdue": hw.due_date < timezone.now(),
            }
        )

    context = {
        'course': course,
        'homework_status': homework_status,
        'total_homeworks': homeworks.count(),
        'submitted_count': my_submissions.count(),
    }
    
    return render(request, 'assignments/course_detail.html', context)


@login_required
@student_required
def homework_detail(request, pk):
    """Детальная страница задания для студента"""
    homework = get_object_or_404(Homework, pk=pk)
    
    # Проверка доступа - студент должен быть записан на курс
    if request.user not in homework.course.students.all():
        messages.error(request, 'У вас нет доступа к этому заданию')
        return redirect('student_dashboard')
    
    submission = Submission.objects.filter(homework=homework, student=request.user).first()

    if request.method == "POST":
        if submission:
            messages.warning(request, "Вы уже отправили работу по этому заданию")
            return redirect("homework_detail", pk=pk)

        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = request.user
            submission.save()
            messages.success(request, 'Работа успешно отправлена!')
            return redirect('course_detail', pk=homework.course.pk)
    else:
        form = SubmissionForm()

    context = {
        "homework": homework,
        "submission": submission,
        "form": form,
        "is_overdue": homework.due_date < timezone.now(),
    }

    return render(request, "assignments/homework_detail.html", context)


@login_required
@student_required
def my_submissions(request):
    """Список всех отправленных работ студента"""
    submissions = Submission.objects.filter(student=request.user).order_by("-submitted_at")

    context = {
        "submissions": submissions,
    }

    return render(request, "assignments/my_submissions.html", context)


@login_required
@student_required
def my_grades(request):
    """Таблица оценок студента по всем курсам"""
    courses = request.user.enrolled_courses.all()
    
    grades_data = []
    for course in courses:
        homeworks = course.homeworks.all().order_by('due_date')
        course_grades = {
            'course': course,
            'homeworks': []
        }
        
        for hw in homeworks:
            submission = Submission.objects.filter(homework=hw, student=request.user).first()
            course_grades['homeworks'].append({
                'homework': hw,
                'submission': submission,
                'grade': submission.grade if submission else None,
                'status': 'Оценено' if submission and submission.grade else 'На проверке' if submission else 'Не сдано'
            })
        
        grades_data.append(course_grades)
    
    context = {
        'grades_data': grades_data,
    }
    
    return render(request, 'assignments/my_grades.html', context)


# ============= Преподаватель =============


@login_required
@teacher_required
def teacher_dashboard(request):
    """Dashboard преподавателя - список его курсов"""
    courses = request.user.teaching_courses.all()
    
    # Статистика
    all_homeworks = Homework.objects.filter(course__in=courses)
    all_submissions = Submission.objects.filter(homework__in=all_homeworks)
    pending_submissions = all_submissions.filter(grade__isnull=True)

    context = {
        'courses': courses,
        'total_courses': courses.count(),
        'total_homeworks': all_homeworks.count(),
        'total_submissions': all_submissions.count(),
        'pending_count': pending_submissions.count(),
    }

    return render(request, "assignments/teacher_dashboard.html", context)


@login_required
@teacher_required
def teacher_course_detail(request, pk):
    """Детальная страница курса для преподавателя"""
    course = get_object_or_404(Course, pk=pk)
    
    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, 'У вас нет доступа к этому курсу')
        return redirect('teacher_dashboard')
    
    homeworks = course.homeworks.all().order_by('-created_at')
    all_submissions = Submission.objects.filter(homework__course=course)
    
    context = {
        'course': course,
        'homeworks': homeworks,
        'students_count': course.students.count(),
        'total_submissions': all_submissions.count(),
        'pending_count': all_submissions.filter(grade__isnull=True).count(),
    }
    
    return render(request, 'assignments/teacher_course_detail.html', context)


@login_required
@teacher_required
def create_course(request):
    """Создание нового курса"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title and description:
            course = Course.objects.create(
                title=title,
                description=description
            )
            course.teachers.add(request.user)
            messages.success(request, f'Курс "{course.title}" успешно создан!')
            return redirect('teacher_course_detail', pk=course.pk)
        else:
            messages.error(request, 'Заполните все обязательные поля')
    
    return render(request, 'assignments/create_course.html')


@login_required
@teacher_required
def edit_course(request, pk):
    """Редактирование курса"""
    course = get_object_or_404(Course, pk=pk)
    
    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, 'У вас нет доступа к этому курсу')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.save()
        messages.success(request, 'Курс успешно обновлен!')
        return redirect('teacher_course_detail', pk=course.pk)
    
    context = {'course': course}
    return render(request, 'assignments/edit_course.html', context)


@login_required
@teacher_required
def manage_students(request, pk):
    """Управление студентами курса"""
    course = get_object_or_404(Course, pk=pk)
    
    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, 'У вас нет доступа к этому курсу')
        return redirect('teacher_dashboard')
    
    from django.contrib.auth.models import User
    all_students = User.objects.filter(profile__role='student')
    current_students = course.students.all()
    
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        course.students.set(User.objects.filter(id__in=student_ids))
        messages.success(request, 'Список студентов обновлен!')
        return redirect('teacher_course_detail', pk=course.pk)
    
    context = {
        'course': course,
        'all_students': all_students,
        'current_students': current_students,
    }
    return render(request, 'assignments/manage_students.html', context)


@login_required
@teacher_required
def teacher_create_homework(request, course_pk):
    """Создание домашнего задания"""
    course = get_object_or_404(Course, pk=course_pk)
    
    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, 'У вас нет доступа к этому курсу')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.course = course
            homework.save()
            messages.success(request, f'Задание "{homework.title}" создано!')
            return redirect('teacher_course_detail', pk=course.pk)
    else:
        form = HomeworkForm()
    
    context = {'form': form, 'course': course}
    return render(request, 'assignments/teacher_create_homework.html', context)


@login_required
@teacher_required
def teacher_edit_homework(request, pk):
    """Редактирование домашнего задания"""
    homework = get_object_or_404(Homework, pk=pk)
    
    # Проверка доступа
    if request.user not in homework.course.teachers.all():
        messages.error(request, 'У вас нет доступа к этому заданию')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задание успешно обновлено!')
            return redirect('teacher_course_detail', pk=homework.course.pk)
    else:
        form = HomeworkForm(instance=homework)
    
    context = {'form': form, 'homework': homework}
    return render(request, 'assignments/teacher_edit_homework.html', context)


@login_required
@teacher_required
def teacher_homework_submissions(request, pk):
    """Список отправок по домашнему заданию"""
    homework = get_object_or_404(Homework, pk=pk)
    
    # Проверка доступа
    if request.user not in homework.course.teachers.all():
        messages.error(request, 'У вас нет доступа к этому заданию')
        return redirect('teacher_dashboard')
    
    submissions = homework.submissions.all().order_by('-submitted_at')
    
    context = {
        'homework': homework,
        'submissions': submissions,
        'total_count': submissions.count(),
        'graded_count': submissions.filter(grade__isnull=False).count(),
        'pending_count': submissions.filter(grade__isnull=True).count(),
    }
    
    return render(request, 'assignments/teacher_homework_submissions.html', context)


@login_required
@teacher_required
def teacher_grade_submission(request, pk):
    """Проверка и выставление оценки"""
    submission = get_object_or_404(Submission, pk=pk)
    
    # Проверка доступа
    if request.user not in submission.homework.course.teachers.all():
        messages.error(request, 'У вас нет доступа к этой работе')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f'Оценка для {submission.student.get_full_name()} выставлена!')
            return redirect('teacher_homework_submissions', pk=submission.homework.pk)
    else:
        form = GradeForm(instance=submission)

    context = {
        "submission": submission,
        "form": form,
    }
    
    return render(request, 'assignments/teacher_grade_submission.html', context)


@login_required
@teacher_required
def teacher_all_submissions(request):
    """Все отправки преподавателя"""
    courses = request.user.teaching_courses.all()
    submissions = Submission.objects.filter(homework__course__in=courses).order_by('-submitted_at')
    
    # Фильтрация
    status_filter = request.GET.get("status", "all")
    if status_filter == "pending":
        submissions = submissions.filter(grade__isnull=True)
    elif status_filter == "graded":
        submissions = submissions.filter(grade__isnull=False)

    context = {
        "submissions": submissions,
        "status_filter": status_filter,
    }
    
    return render(request, 'assignments/teacher_all_submissions.html', context)


# ============= Общие =============


def home_view(request):
    """Главная страница для неавторизованных пользователей"""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "assignments/home.html")
