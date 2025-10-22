from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Homework, Submission
from .forms import RegisterForm, HomeworkForm, SubmissionForm, GradeForm
from .decorators import student_required, teacher_required


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
    """Dashboard студента"""
    homeworks = Homework.objects.all().order_by("-created_at")
    my_submissions = Submission.objects.filter(student=request.user)

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
        "homework_status": homework_status,
        "total_homeworks": homeworks.count(),
        "submitted_count": my_submissions.count(),
        "graded_count": my_submissions.filter(grade__isnull=False).count(),
    }

    return render(request, "assignments/student_dashboard.html", context)


@login_required
@student_required
def homework_detail(request, pk):
    """Детальная страница задания для студента"""
    homework = get_object_or_404(Homework, pk=pk)
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
            messages.success(request, "Работа успешно отправлена!")
            return redirect("student_dashboard")
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


# ============= Преподаватель =============


@login_required
@teacher_required
def teacher_dashboard(request):
    """Dashboard преподавателя"""
    homeworks = Homework.objects.all().order_by("-created_at")
    all_submissions = Submission.objects.all().order_by("-submitted_at")
    pending_submissions = all_submissions.filter(grade__isnull=True)

    context = {
        "homeworks": homeworks,
        "recent_submissions": all_submissions[:10],
        "pending_count": pending_submissions.count(),
        "total_homeworks": homeworks.count(),
        "total_submissions": all_submissions.count(),
    }

    return render(request, "assignments/teacher_dashboard.html", context)


@login_required
@teacher_required
def create_homework(request):
    """Создание нового домашнего задания"""
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save()
            messages.success(request, f'Задание "{homework.title}" успешно создано!')
            return redirect("teacher_dashboard")
    else:
        form = HomeworkForm()

    return render(request, "assignments/create_homework.html", {"form": form})


@login_required
@teacher_required
def edit_homework(request, pk):
    """Редактирование домашнего задания"""
    homework = get_object_or_404(Homework, pk=pk)

    if request.method == "POST":
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            messages.success(request, "Задание успешно обновлено!")
            return redirect("homework_submissions", pk=pk)
    else:
        form = HomeworkForm(instance=homework)

    return render(request, "assignments/edit_homework.html", {"form": form, "homework": homework})


@login_required
@teacher_required
def delete_homework(request, pk):
    """Удаление домашнего задания"""
    homework = get_object_or_404(Homework, pk=pk)

    if request.method == "POST":
        title = homework.title
        homework.delete()
        messages.success(request, f'Задание "{title}" удалено')
        return redirect("teacher_dashboard")

    return render(request, "assignments/delete_homework.html", {"homework": homework})


@login_required
@teacher_required
def homework_submissions(request, pk):
    """Список всех отправок по конкретному заданию"""
    homework = get_object_or_404(Homework, pk=pk)
    submissions = Submission.objects.filter(homework=homework).order_by("-submitted_at")

    context = {
        "homework": homework,
        "submissions": submissions,
        "total_submissions": submissions.count(),
        "graded_count": submissions.filter(grade__isnull=False).count(),
        "pending_count": submissions.filter(grade__isnull=True).count(),
    }

    return render(request, "assignments/homework_submissions.html", context)


@login_required
@teacher_required
def grade_submission(request, pk):
    """Проверка и выставление оценки за работу"""
    submission = get_object_or_404(Submission, pk=pk)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f"Оценка для {submission.student.get_full_name()} выставлена!")
            return redirect("homework_submissions", pk=submission.homework.pk)
    else:
        form = GradeForm(instance=submission)

    context = {
        "submission": submission,
        "form": form,
    }

    return render(request, "assignments/grade_submission.html", context)


@login_required
@teacher_required
def all_submissions(request):
    """Все отправленные работы (для преподавателя)"""
    submissions = Submission.objects.all().order_by("-submitted_at")

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

    return render(request, "assignments/all_submissions.html", context)


# ============= Общие =============


def home_view(request):
    """Главная страница для неавторизованных пользователей"""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "assignments/home.html")
