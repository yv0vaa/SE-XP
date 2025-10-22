"""
Представления (views) для системы проверки домашних заданий.

Содержит все представления для:
- Авторизации и регистрации пользователей
- Dashboard студента и преподавателя
- Управления домашними заданиями
- Отправки и проверки работ
"""

import os

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import student_required, teacher_required
from .forms import GradeForm, HomeworkForm, RegisterForm, SubmissionForm
from .models import Course, CourseEnrollmentRequest, Homework, Submission

User = get_user_model()

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
    if request.user.profile.is_teacher:
        return redirect("teacher_dashboard")
    return redirect("login")


# ============= Студент =============


@login_required
@student_required
def student_dashboard(request):
    """Dashboard студента - список курсов"""
    courses = request.user.enrolled_courses.all()

    # Статистика по всем курсам
    all_homeworks = Homework.objects.filter(course__in=courses)
    student_submissions = Submission.objects.filter(student=request.user)

    context = {
        "courses": courses,
        "total_courses": courses.count(),
        "total_homeworks": all_homeworks.count(),
        "submitted_count": student_submissions.count(),
        "graded_count": student_submissions.filter(grade__isnull=False).count(),
    }

    return render(request, "assignments/student_dashboard.html", context)


@login_required
@student_required
def course_detail(request, pk):
    """Детальная страница курса для студента"""
    course = get_object_or_404(Course, pk=pk)

    # Проверка доступа - студент должен быть записан на курс
    if request.user not in course.students.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("student_dashboard")

    homeworks = course.homeworks.all().order_by("-created_at")
    course_submissions = Submission.objects.filter(student=request.user, homework__course=course)

    # Добавляем информацию о том, сдал ли студент каждое ДЗ
    homework_status = []
    for hw in homeworks:
        submission = course_submissions.filter(homework=hw).first()
        homework_status.append(
            {
                "homework": hw,
                "submission": submission,
                "is_overdue": hw.due_date < timezone.now(),
            }
        )

    context = {
        "course": course,
        "homework_status": homework_status,
        "total_homeworks": homeworks.count(),
        "submitted_count": course_submissions.count(),
    }

    return render(request, "assignments/course_detail.html", context)


@login_required
@student_required
def homework_detail(request, pk):
    """Детальная страница задания для студента"""
    homework = get_object_or_404(Homework, pk=pk)

    # Проверка доступа - студент должен быть записан на курс
    if request.user not in homework.course.students.all():
        messages.error(request, "У вас нет доступа к этому заданию")
        return redirect("student_dashboard")

    submission = Submission.objects.filter(homework=homework, student=request.user).first()

    if request.method == "POST":
        # Разрешаем переотправку работы (замену файла)
        if submission:
            # Обновляем существующую отправку
            form = SubmissionForm(request.POST, request.FILES, instance=submission)
            if form.is_valid():
                # Удаляем старый файл перед сохранением нового
                if submission.solution_file and os.path.isfile(submission.solution_file.path):
                    os.remove(submission.solution_file.path)

                submission = form.save(commit=False)
                # Сбрасываем оценку при переотправке
                submission.grade = None
                submission.feedback = ""
                submission.save()
                messages.success(request, "Работа успешно переотправлена! Оценка сброшена.")
                return redirect("course_detail", pk=homework.course.pk)
        else:
            # Создаём новую отправку
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.homework = homework
                submission.student = request.user
                submission.save()
                messages.success(request, "Работа успешно отправлена!")
                return redirect("course_detail", pk=homework.course.pk)
    else:
        form = SubmissionForm(instance=submission) if submission else SubmissionForm()

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
        homeworks = course.homeworks.all().order_by("due_date")
        course_grades = {"course": course, "homeworks": []}

        for hw in homeworks:
            submission = Submission.objects.filter(homework=hw, student=request.user).first()
            course_grades["homeworks"].append(
                {
                    "homework": hw,
                    "submission": submission,
                    "grade": submission.grade if submission else None,
                    "status": ("Оценено" if submission and submission.grade else "На проверке" if submission else "Не сдано"),
                }
            )

        grades_data.append(course_grades)

    context = {
        "grades_data": grades_data,
    }

    return render(request, "assignments/my_grades.html", context)


@login_required
@student_required
def available_courses(request):
    """Список всех доступных курсов для студента"""
    # Курсы, на которые студент уже записан
    enrolled_courses = request.user.enrolled_courses.all()

    # Все курсы
    all_courses = Course.objects.all()

    # Заявки студента
    student_requests = CourseEnrollmentRequest.objects.filter(student=request.user)
    requests_dict = {req.course_id: req for req in student_requests}

    # Подготавливаем информацию о каждом курсе
    courses_info = []
    for course in all_courses:
        is_enrolled = course in enrolled_courses
        request_status = None
        enrollment_request = requests_dict.get(course.id)

        if enrollment_request:
            request_status = enrollment_request.status

        courses_info.append(
            {
                "course": course,
                "is_enrolled": is_enrolled,
                "request_status": request_status,
                "request_id": enrollment_request.id if enrollment_request else None,
            }
        )

    context = {
        "courses_info": courses_info,
    }

    return render(request, "assignments/available_courses.html", context)


@login_required
@student_required
def request_enrollment(request, course_pk):
    """Подать заявку на зачисление на курс"""
    course = get_object_or_404(Course, pk=course_pk)

    # Проверяем, не записан ли студент уже на курс
    if request.user in course.students.all():
        messages.warning(request, "Вы уже записаны на этот курс")
        return redirect("available_courses")

    # Проверяем, нет ли уже активной заявки
    existing_request = CourseEnrollmentRequest.objects.filter(course=course, student=request.user, status="pending").first()

    if existing_request:
        messages.warning(request, "Вы уже подали заявку на этот курс")
        return redirect("available_courses")

    if request.method == "POST":
        message = request.POST.get("message", "")
        CourseEnrollmentRequest.objects.create(course=course, student=request.user, message=message)
        messages.success(request, f'Заявка на курс "{course.title}" успешно подана!')
        return redirect("available_courses")

    context = {"course": course}
    return render(request, "assignments/request_enrollment.html", context)


@login_required
@student_required
def cancel_enrollment_request(request, request_pk):
    """Отменить заявку на зачисление"""
    enrollment_request = get_object_or_404(CourseEnrollmentRequest, pk=request_pk)

    # Проверка доступа
    if enrollment_request.student != request.user:
        messages.error(request, "У вас нет доступа к этой заявке")
        return redirect("available_courses")

    # Можно отменить только заявки со статусом "pending"
    if enrollment_request.status != "pending":
        messages.error(request, "Эту заявку нельзя отменить")
        return redirect("available_courses")

    if request.method == "POST":
        course_title = enrollment_request.course.title
        enrollment_request.delete()
        messages.success(request, f'Заявка на курс "{course_title}" отменена')
        return redirect("available_courses")

    return redirect("available_courses")


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
        "courses": courses,
        "total_courses": courses.count(),
        "total_homeworks": all_homeworks.count(),
        "total_submissions": all_submissions.count(),
        "pending_count": pending_submissions.count(),
    }

    return render(request, "assignments/teacher_dashboard.html", context)


@login_required
@teacher_required
def teacher_course_detail(request, pk):
    """Детальная страница курса для преподавателя"""
    course = get_object_or_404(Course, pk=pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    homeworks = course.homeworks.all().order_by("-created_at")
    all_submissions = Submission.objects.filter(homework__course=course)

    context = {
        "course": course,
        "homeworks": homeworks,
        "students_count": course.students.count(),
        "total_submissions": all_submissions.count(),
        "pending_count": all_submissions.filter(grade__isnull=True).count(),
    }

    return render(request, "assignments/teacher_course_detail.html", context)


@login_required
@teacher_required
def create_course(request):
    """Создание нового курса"""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if title and description:
            course = Course.objects.create(title=title, description=description)
            course.teachers.add(request.user)
            messages.success(request, f'Курс "{course.title}" успешно создан!')
            return redirect("teacher_course_detail", pk=course.pk)
        messages.error(request, "Заполните все обязательные поля")

    return render(request, "assignments/create_course.html")


@login_required
@teacher_required
def edit_course(request, pk):
    """Редактирование курса"""
    course = get_object_or_404(Course, pk=pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        course.title = request.POST.get("title", course.title)
        course.description = request.POST.get("description", course.description)
        course.save()
        messages.success(request, "Курс успешно обновлен!")
        return redirect("teacher_course_detail", pk=course.pk)

    context = {"course": course}
    return render(request, "assignments/edit_course.html", context)


@login_required
@teacher_required
def manage_students(request, pk):
    """Управление студентами курса - просмотр зачисленных студентов и заявок"""
    course = get_object_or_404(Course, pk=pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    # Текущие студенты
    current_students = course.students.all()

    # Заявки на зачисление
    pending_requests = CourseEnrollmentRequest.objects.filter(course=course, status="pending").order_by("-created_at")

    # История заявок (одобренные и отклоненные)
    processed_requests = CourseEnrollmentRequest.objects.filter(course=course, status__in=["approved", "rejected"]).order_by(
        "-processed_at"
    )[
        :20
    ]  # Показываем последние 20

    context = {
        "course": course,
        "current_students": current_students,
        "pending_requests": pending_requests,
        "processed_requests": processed_requests,
        "pending_count": pending_requests.count(),
    }
    return render(request, "assignments/manage_students.html", context)


@login_required
@teacher_required
def approve_enrollment_request(request, request_pk):
    """Одобрить заявку на зачисление"""
    enrollment_request = get_object_or_404(CourseEnrollmentRequest, pk=request_pk)

    # Проверка доступа
    if request.user not in enrollment_request.course.teachers.all():
        messages.error(request, "У вас нет доступа к этой заявке")
        return redirect("teacher_dashboard")

    # Проверка статуса
    if enrollment_request.status != "pending":
        messages.warning(request, "Эта заявка уже обработана")
        return redirect("manage_students", pk=enrollment_request.course.pk)

    if request.method == "POST":
        # Обновляем статус заявки
        enrollment_request.status = "approved"
        enrollment_request.processed_at = timezone.now()
        enrollment_request.processed_by = request.user
        enrollment_request.save()

        # Добавляем студента на курс
        enrollment_request.course.students.add(enrollment_request.student)

        messages.success(
            request,
            f'Студент {enrollment_request.student.get_full_name()} зачислен на курс "{enrollment_request.course.title}"',
        )
        return redirect("manage_students", pk=enrollment_request.course.pk)

    return redirect("manage_students", pk=enrollment_request.course.pk)


@login_required
@teacher_required
def reject_enrollment_request(request, request_pk):
    """Отклонить заявку на зачисление"""
    enrollment_request = get_object_or_404(CourseEnrollmentRequest, pk=request_pk)

    # Проверка доступа
    if request.user not in enrollment_request.course.teachers.all():
        messages.error(request, "У вас нет доступа к этой заявке")
        return redirect("teacher_dashboard")

    # Проверка статуса
    if enrollment_request.status != "pending":
        messages.warning(request, "Эта заявка уже обработана")
        return redirect("manage_students", pk=enrollment_request.course.pk)

    if request.method == "POST":
        # Обновляем статус заявки
        enrollment_request.status = "rejected"
        enrollment_request.processed_at = timezone.now()
        enrollment_request.processed_by = request.user
        enrollment_request.save()

        messages.info(request, f"Заявка от {enrollment_request.student.get_full_name()} отклонена")
        return redirect("manage_students", pk=enrollment_request.course.pk)

    return redirect("manage_students", pk=enrollment_request.course.pk)


@login_required
@teacher_required
def remove_student_from_course(request, course_pk, student_pk):
    """Удалить студента с курса"""
    course = get_object_or_404(Course, pk=course_pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    student = get_object_or_404(User, pk=student_pk)

    if request.method == "POST":
        course.students.remove(student)
        messages.success(request, f"Студент {student.get_full_name()} удален с курса")
        return redirect("manage_students", pk=course.pk)

    return redirect("manage_students", pk=course.pk)


@login_required
@teacher_required
def teacher_create_homework(request, course_pk):
    """Создание домашнего задания"""
    course = get_object_or_404(Course, pk=course_pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.course = course
            homework.save()
            messages.success(request, f'Задание "{homework.title}" создано!')
            return redirect("teacher_course_detail", pk=course.pk)
    else:
        form = HomeworkForm()

    context = {"form": form, "course": course}
    return render(request, "assignments/teacher_create_homework.html", context)


@login_required
@teacher_required
def teacher_edit_homework(request, pk):
    """Редактирование домашнего задания"""
    homework = get_object_or_404(Homework, pk=pk)

    # Проверка доступа
    if request.user not in homework.course.teachers.all():
        messages.error(request, "У вас нет доступа к этому заданию")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            messages.success(request, "Задание успешно обновлено!")
            return redirect("teacher_course_detail", pk=homework.course.pk)
    else:
        form = HomeworkForm(instance=homework)

    context = {"form": form, "homework": homework}
    return render(request, "assignments/teacher_edit_homework.html", context)


@login_required
@teacher_required
def teacher_homework_submissions(request, pk):
    """Список отправок по домашнему заданию"""
    homework = get_object_or_404(Homework, pk=pk)

    # Проверка доступа
    if request.user not in homework.course.teachers.all():
        messages.error(request, "У вас нет доступа к этому заданию")
        return redirect("teacher_dashboard")

    submissions = homework.submissions.all().order_by("-submitted_at")

    context = {
        "homework": homework,
        "submissions": submissions,
        "total_count": submissions.count(),
        "graded_count": submissions.filter(grade__isnull=False).count(),
        "pending_count": submissions.filter(grade__isnull=True).count(),
    }

    return render(request, "assignments/teacher_homework_submissions.html", context)


@login_required
@teacher_required
def teacher_grade_submission(request, pk):
    """Проверка и выставление оценки"""
    submission = get_object_or_404(Submission, pk=pk)

    # Проверка доступа
    if request.user not in submission.homework.course.teachers.all():
        messages.error(request, "У вас нет доступа к этой работе")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f"Оценка для {submission.student.get_full_name()} выставлена!")
            return redirect("teacher_homework_submissions", pk=submission.homework.pk)
    else:
        form = GradeForm(instance=submission)

    context = {
        "submission": submission,
        "form": form,
    }

    return render(request, "assignments/teacher_grade_submission.html", context)


@login_required
@teacher_required
def teacher_all_submissions(request):
    """Все отправки преподавателя"""
    courses = request.user.teaching_courses.all()
    submissions = Submission.objects.filter(homework__course__in=courses).order_by("-submitted_at")

    # Фильтрация
    status_filter = request.GET.get("status", "all")
    course_filter = request.GET.get("course", "all")

    if status_filter == "pending":
        submissions = submissions.filter(grade__isnull=True)
    elif status_filter == "graded":
        submissions = submissions.filter(grade__isnull=False)

    if course_filter != "all":
        submissions = submissions.filter(homework__course_id=course_filter)

    context = {
        "submissions": submissions,
        "status_filter": status_filter,
        "course_filter": course_filter,
        "courses": courses,
    }

    return render(request, "assignments/teacher_all_submissions.html", context)


@login_required
@teacher_required
def delete_course(request, pk):
    """Удаление курса"""
    course = get_object_or_404(Course, pk=pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        course_title = course.title
        course.delete()
        messages.success(request, f'Курс "{course_title}" успешно удалён!')
        return redirect("teacher_dashboard")

    return redirect("teacher_course_detail", pk=pk)


@login_required
@teacher_required
def delete_homework(request, pk):
    """Удаление домашнего задания"""
    homework = get_object_or_404(Homework, pk=pk)

    # Проверка доступа
    if request.user not in homework.course.teachers.all():
        messages.error(request, "У вас нет доступа к этому заданию")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        course_pk = homework.course.pk
        homework_title = homework.title
        homework.delete()
        messages.success(request, f'Задание "{homework_title}" успешно удалено!')
        return redirect("teacher_course_detail", pk=course_pk)

    return redirect("teacher_course_detail", pk=homework.course.pk)


@login_required
@teacher_required
def teacher_grades_table(request, course_pk):
    """Сводная таблица оценок студентов по курсу"""
    course = get_object_or_404(Course, pk=course_pk)

    # Проверка доступа
    if request.user not in course.teachers.all():
        messages.error(request, "У вас нет доступа к этому курсу")
        return redirect("teacher_dashboard")

    # Получаем всех студентов курса и все задания
    students = course.students.all().order_by("last_name", "first_name")
    homeworks = course.homeworks.all().order_by("due_date")

    # Формируем таблицу оценок
    grades_table = []
    for student in students:
        student_row = {
            "student": student,
            "grades": [],
            "total": 0,
            "average": 0,
            "completed": 0,
        }

        total_grade = 0
        graded_count = 0

        for hw in homeworks:
            submission = Submission.objects.filter(homework=hw, student=student).first()
            grade_info = {
                "homework": hw,
                "submission": submission,
                "grade": submission.grade if submission else None,
                "status": (
                    "graded" if submission and submission.grade is not None else "submitted" if submission else "missing"
                ),
            }
            student_row["grades"].append(grade_info)

            if submission and submission.grade is not None:
                total_grade += submission.grade
                graded_count += 1

        if graded_count > 0:
            student_row["average"] = round(total_grade / graded_count, 1)
        student_row["completed"] = graded_count
        student_row["total"] = total_grade

        grades_table.append(student_row)

    context = {
        "course": course,
        "homeworks": homeworks,
        "grades_table": grades_table,
        "students_count": students.count(),
        "homeworks_count": homeworks.count(),
    }

    return render(request, "assignments/teacher_grades_table.html", context)


# ============= Общие =============


def home_view(request):
    """Главная страница для неавторизованных пользователей"""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "assignments/home.html")
