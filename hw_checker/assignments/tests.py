"""
Comprehensive test suite for the Homework Checker application.
Tests follow TDD principles covering models, views, forms, and decorators.
"""

import tempfile
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import GradeForm, HomeworkForm, RegisterForm, SubmissionForm
from .models import Course, Homework, Submission, UserProfile

User = get_user_model()

# ============================================================================
# MODEL TESTS
# ============================================================================


class UserProfileModelTest(TestCase):
    """Tests for UserProfile model"""

    def setUp(self):
        """Set up test users"""
        self.student_user = User.objects.create_user(
            username="student1", password="test123", first_name="John", last_name="Doe"
        )
        self.teacher_user = User.objects.create_user(
            username="teacher1", password="test123", first_name="Jane", last_name="Smith"
        )

    def test_user_profile_created_on_user_creation(self):
        """Test that UserProfile is automatically created when User is created"""
        self.assertTrue(hasattr(self.student_user, "profile"))
        self.assertIsInstance(self.student_user.profile, UserProfile)

    def test_user_profile_default_role_is_student(self):
        """Test that default role is 'student'"""
        self.assertEqual(self.student_user.profile.role, "student")

    def test_user_profile_str_representation(self):
        """Test __str__ method returns correct format"""
        expected = f"{self.student_user.username} - Студент"
        self.assertEqual(str(self.student_user.profile), expected)

    def test_is_student_property(self):
        """Test is_student property returns correct value"""
        self.assertTrue(self.student_user.profile.is_student)
        self.teacher_user.profile.role = "teacher"
        self.teacher_user.profile.save()
        self.assertFalse(self.teacher_user.profile.is_student)

    def test_is_teacher_property(self):
        """Test is_teacher property returns correct value"""
        self.assertFalse(self.student_user.profile.is_teacher)
        self.teacher_user.profile.role = "teacher"
        self.teacher_user.profile.save()
        self.assertTrue(self.teacher_user.profile.is_teacher)

    def test_role_choices_validation(self):
        """Test that role field accepts only valid choices"""
        profile = self.student_user.profile
        profile.role = "student"
        profile.save()
        self.assertEqual(profile.role, "student")
        profile.role = "teacher"
        profile.save()
        self.assertEqual(profile.role, "teacher")


class HomeworkModelTest(TestCase):
    """Tests for Homework model"""

    def setUp(self):
        """Set up test homework"""
        # Create a teacher and course first
        self.teacher = User.objects.create_user(username="teacher", password="test123")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

        self.course = Course.objects.create(title="Test Course", description="Test course description")
        self.course.teachers.add(self.teacher)

        self.homework = Homework.objects.create(
            course=self.course,
            title="Test Assignment",
            description="This is a test assignment",
            due_date=timezone.now() + timedelta(days=7),
        )

    def test_homework_creation(self):
        """Test homework can be created with required fields"""
        self.assertIsInstance(self.homework, Homework)
        self.assertEqual(self.homework.title, "Test Assignment")

    def test_homework_str_representation(self):
        """Test __str__ method returns course and title"""
        self.assertEqual(str(self.homework), "Test Course - Test Assignment")

    def test_homework_ordering(self):
        """Test homeworks are ordered by created_at descending"""
        hw1 = Homework.objects.create(
            course=self.course, title="First", description="First assignment", due_date=timezone.now() + timedelta(days=1)
        )
        hw2 = Homework.objects.create(
            course=self.course, title="Second", description="Second assignment", due_date=timezone.now() + timedelta(days=2)
        )
        homeworks = list(Homework.objects.all())
        self.assertEqual(homeworks[0], hw2)
        self.assertEqual(homeworks[1], hw1)

    def test_homework_has_created_at_timestamp(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.homework.created_at)
        self.assertLessEqual(self.homework.created_at, timezone.now())


class SubmissionModelTest(TestCase):
    """Tests for Submission model"""

    def setUp(self):
        """Set up test data"""
        self.student = User.objects.create_user(username="student", password="test123")

        # Create teacher and course
        self.teacher = User.objects.create_user(username="teacher", password="test123")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

        self.course = Course.objects.create(title="Test Course", description="Test course description")
        self.course.teachers.add(self.teacher)

        self.homework = Homework.objects.create(
            course=self.course, title="Test HW", description="Test", due_date=timezone.now() + timedelta(days=7)
        )
        self.file = SimpleUploadedFile("test.txt", b"file content", content_type="text/plain")

    def test_submission_creation(self):
        """Test submission can be created"""
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        self.assertIsInstance(submission, Submission)
        self.assertEqual(submission.student, self.student)
        self.assertEqual(submission.homework, self.homework)

    def test_submission_str_representation(self):
        """Test __str__ method format"""
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        expected = f"{self.student.username} - {self.homework.title}"
        self.assertEqual(str(submission), expected)

    def test_submission_has_submitted_at_timestamp(self):
        """Test submitted_at is automatically set"""
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        self.assertIsNotNone(submission.submitted_at)
        self.assertLessEqual(submission.submitted_at, timezone.now())

    def test_submission_grade_is_optional(self):
        """Test grade field can be null"""
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        self.assertIsNone(submission.grade)

    def test_submission_feedback_is_optional(self):
        """Test feedback field can be blank"""
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        self.assertEqual(submission.feedback, "")

    def test_submission_unique_together_constraint(self):
        """Test that a student can only submit once per homework"""
        Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        # Create another file for second submission
        file2 = SimpleUploadedFile("test2.txt", b"file content 2", content_type="text/plain")
        with self.assertRaises(Exception):
            Submission.objects.create(homework=self.homework, student=self.student, solution_file=file2)

    def test_submission_ordering(self):
        """Test submissions are ordered by submitted_at descending"""
        student2 = User.objects.create_user(username="student2", password="test123")
        file2 = SimpleUploadedFile("test2.txt", b"file content 2", content_type="text/plain")
        sub1 = Submission.objects.create(homework=self.homework, student=self.student, solution_file=self.file)
        sub2 = Submission.objects.create(homework=self.homework, student=student2, solution_file=file2)
        submissions = list(Submission.objects.all())
        self.assertEqual(submissions[0], sub2)
        self.assertEqual(submissions[1], sub1)


# ============================================================================
# FORM TESTS
# ============================================================================


class RegisterFormTest(TestCase):
    """Tests for RegisterForm"""

    def test_register_form_valid_data(self):
        """Test form is valid with correct data"""
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "role": "student",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_missing_email(self):
        """Test form is invalid without email"""
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "role": "student",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_form_missing_role(self):
        """Test form is invalid without role"""
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_form_password_mismatch(self):
        """Test form is invalid when passwords don't match"""
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "TestPass123!",
            "password2": "DifferentPass123!",
            "role": "student",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_form_saves_user_with_profile(self):
        """Test that saving form creates user and sets profile role"""
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "role": "teacher",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.profile.role, "teacher")


class HomeworkFormTest(TestCase):
    """Tests for HomeworkForm"""

    def test_homework_form_valid_data(self):
        """Test form is valid with correct data"""
        form_data = {
            "title": "New Assignment",
            "description": "This is a new assignment",
            "due_date": timezone.now() + timedelta(days=7),
        }
        form = HomeworkForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_homework_form_missing_title(self):
        """Test form is invalid without title"""
        form_data = {
            "description": "This is a new assignment",
            "due_date": timezone.now() + timedelta(days=7),
        }
        form = HomeworkForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_homework_form_missing_description(self):
        """Test form is invalid without description"""
        form_data = {
            "title": "New Assignment",
            "due_date": timezone.now() + timedelta(days=7),
        }
        form = HomeworkForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_homework_form_saves_correctly(self):
        """Test form saves homework correctly"""
        # Create a course and teacher first
        teacher = User.objects.create_user(username="teacher", password="test123")
        teacher.profile.role = "teacher"
        teacher.profile.save()

        course = Course.objects.create(title="Test Course", description="Test course description")
        course.teachers.add(teacher)

        form_data = {
            "title": "New Assignment",
            "description": "This is a new assignment",
            "due_date": timezone.now() + timedelta(days=7),
        }
        form = HomeworkForm(data=form_data)
        self.assertTrue(form.is_valid())
        homework = form.save(commit=False)
        homework.course = course
        homework.save()
        self.assertEqual(homework.title, "New Assignment")


class SubmissionFormTest(TestCase):
    """Tests for SubmissionForm"""

    def test_submission_form_valid_with_file(self):
        """Test form is valid with a file"""
        file = SimpleUploadedFile("solution.txt", b"my solution", content_type="text/plain")
        form = SubmissionForm(files={"solution_file": file})
        self.assertTrue(form.is_valid())

    def test_submission_form_invalid_without_file(self):
        """Test form is invalid without a file"""
        form = SubmissionForm(data={})
        self.assertFalse(form.is_valid())


class GradeFormTest(TestCase):
    """Tests for GradeForm"""

    def test_grade_form_valid_data(self):
        """Test form is valid with grade and feedback"""
        form_data = {"grade": 85, "feedback": "Good work!"}
        form = GradeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_grade_form_valid_without_feedback(self):
        """Test form is valid with just grade"""
        form_data = {"grade": 85, "feedback": ""}
        form = GradeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_grade_form_saves_correctly(self):
        """Test form updates submission grade"""
        student = User.objects.create_user(username="student", password="test123")

        # Create teacher and course
        teacher = User.objects.create_user(username="teacher", password="test123")
        teacher.profile.role = "teacher"
        teacher.profile.save()

        course = Course.objects.create(title="Test Course", description="Test course description")
        course.teachers.add(teacher)

        homework = Homework.objects.create(
            course=course, title="Test", description="Test", due_date=timezone.now() + timedelta(days=7)
        )
        file = SimpleUploadedFile("test.txt", b"content", content_type="text/plain")
        submission = Submission.objects.create(homework=homework, student=student, solution_file=file)

        form_data = {"grade": 90, "feedback": "Excellent!"}
        form = GradeForm(data=form_data, instance=submission)
        self.assertTrue(form.is_valid())
        updated_submission = form.save()
        self.assertEqual(updated_submission.grade, 90)
        self.assertEqual(updated_submission.feedback, "Excellent!")


# ============================================================================
# VIEW TESTS
# ============================================================================


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AuthViewsTest(TestCase):
    """Tests for authentication views"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="test123", first_name="Test", last_name="User")

    def test_home_view_unauthenticated(self):
        """Test home view accessible for unauthenticated users"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/home.html")

    def test_home_view_redirects_authenticated_users(self):
        """Test home view redirects authenticated users to dashboard"""
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_register_view_get(self):
        """Test register view displays form"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/register.html")
        self.assertIsInstance(response.context["form"], RegisterForm)

    def test_register_view_post_valid(self):
        """Test user registration with valid data"""
        form_data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "role": "student",
        }
        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_user = User.objects.get(username="newuser")
        self.assertEqual(new_user.profile.role, "student")

    def test_register_view_redirects_authenticated_users(self):
        """Test register view redirects authenticated users"""
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)

    def test_login_view_get(self):
        """Test login view displays form"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/login.html")

    def test_login_view_post_valid_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "test123"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_redirects_authenticated_users(self):
        """Test login view redirects authenticated users"""
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        """Test logout functionality"""
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_logout_view_requires_authentication(self):
        """Test logout view requires authentication"""
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DashboardViewTest(TestCase):
    """Tests for dashboard view"""

    def setUp(self):
        """Set up test users"""
        self.client = Client()
        self.student = User.objects.create_user(username="student", password="test123")
        self.teacher = User.objects.create_user(username="teacher", password="test123")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

    def test_dashboard_redirects_student(self):
        """Test dashboard redirects student to student dashboard"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("student_dashboard"))

    def test_dashboard_redirects_teacher(self):
        """Test dashboard redirects teacher to teacher dashboard"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("teacher_dashboard"))

    def test_dashboard_requires_authentication(self):
        """Test dashboard requires login"""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class StudentViewsTest(TestCase):
    """Tests for student views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.student = User.objects.create_user(username="student", password="test123")
        self.teacher = User.objects.create_user(username="teacher", password="test123")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

        # Create course
        self.course = Course.objects.create(title="Test Course", description="Test course description")
        self.course.teachers.add(self.teacher)
        self.course.students.add(self.student)

        self.homework = Homework.objects.create(
            course=self.course, title="Test Assignment", description="Description", due_date=timezone.now() + timedelta(days=7)
        )

    def test_student_dashboard_requires_login(self):
        """Test student dashboard requires login"""
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_student_dashboard_requires_student_role(self):
        """Test student dashboard requires student role"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_student_dashboard_accessible_to_students(self):
        """Test student dashboard accessible to students"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/student_dashboard.html")

    def test_student_dashboard_shows_courses(self):
        """Test student dashboard displays course list"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("student_dashboard"))
        self.assertIn("courses", response.context)
        self.assertEqual(len(response.context["courses"]), 1)
        self.assertIn("total_homeworks", response.context)
        self.assertEqual(response.context["total_homeworks"], 1)

    def test_homework_detail_view_get(self):
        """Test homework detail view displays correctly"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("homework_detail", kwargs={"pk": self.homework.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/homework_detail.html")
        self.assertEqual(response.context["homework"], self.homework)

    def test_homework_detail_submission_post(self):
        """Test student can submit homework"""
        self.client.login(username="student", password="test123")
        file = SimpleUploadedFile("solution.txt", b"my solution", content_type="text/plain")
        response = self.client.post(reverse("homework_detail", kwargs={"pk": self.homework.pk}), {"solution_file": file})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Submission.objects.filter(homework=self.homework, student=self.student).exists())

    def test_homework_detail_prevents_duplicate_submission(self):
        """Test student cannot submit same homework twice"""
        self.client.login(username="student", password="test123")
        file1 = SimpleUploadedFile("solution1.txt", b"my solution", content_type="text/plain")
        Submission.objects.create(homework=self.homework, student=self.student, solution_file=file1)

        file2 = SimpleUploadedFile("solution2.txt", b"another solution", content_type="text/plain")
        response = self.client.post(reverse("homework_detail", kwargs={"pk": self.homework.pk}), {"solution_file": file2})
        self.assertEqual(Submission.objects.filter(homework=self.homework, student=self.student).count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("course_detail", kwargs={"pk": self.homework.course.pk}))

    def test_my_submissions_view(self):
        """Test my submissions view shows student's submissions"""
        self.client.login(username="student", password="test123")
        file = SimpleUploadedFile("solution.txt", b"my solution", content_type="text/plain")
        Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)

        response = self.client.get(reverse("my_submissions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/my_submissions.html")
        self.assertEqual(len(response.context["submissions"]), 1)

    def test_my_submissions_requires_student_role(self):
        """Test my submissions requires student role"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("my_submissions"))
        self.assertEqual(response.status_code, 302)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TeacherViewsTest(TestCase):
    """Tests for teacher views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.student = User.objects.create_user(username="student", password="test123")
        self.teacher = User.objects.create_user(username="teacher", password="test123")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

        # Create course
        self.course = Course.objects.create(title="Test Course", description="Test course description")
        self.course.teachers.add(self.teacher)
        self.course.students.add(self.student)

        self.homework = Homework.objects.create(
            course=self.course, title="Test Assignment", description="Description", due_date=timezone.now() + timedelta(days=7)
        )

    def test_teacher_dashboard_requires_login(self):
        """Test teacher dashboard requires login"""
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_teacher_dashboard_requires_teacher_role(self):
        """Test teacher dashboard requires teacher role"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_teacher_dashboard_accessible_to_teachers(self):
        """Test teacher dashboard accessible to teachers"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/teacher_dashboard.html")

    def test_create_homework_view_get(self):
        """Test create homework view displays form"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("teacher_create_homework", kwargs={"course_pk": self.course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/teacher_create_homework.html")
        self.assertIsInstance(response.context["form"], HomeworkForm)

    def test_create_homework_view_post(self):
        """Test creating homework via POST"""
        self.client.login(username="teacher", password="test123")
        form_data = {
            "title": "New Homework",
            "description": "New Description",
            "due_date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M"),
        }
        response = self.client.post(reverse("teacher_create_homework", kwargs={"course_pk": self.course.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Homework.objects.filter(title="New Homework").exists())

    def test_create_homework_requires_teacher_role(self):
        """Test create homework requires teacher role"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("teacher_create_homework", kwargs={"course_pk": self.course.pk}))
        self.assertEqual(response.status_code, 302)

    def test_edit_homework_view_get(self):
        """Test edit homework view displays form"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("teacher_edit_homework", kwargs={"pk": self.homework.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/teacher_edit_homework.html")

    def test_edit_homework_view_post(self):
        """Test editing homework via POST"""
        self.client.login(username="teacher", password="test123")
        form_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "due_date": (timezone.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M"),
        }
        response = self.client.post(reverse("teacher_edit_homework", kwargs={"pk": self.homework.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.homework.refresh_from_db()
        self.assertEqual(self.homework.title, "Updated Title")

    # NOTE: Delete homework feature was removed in course-based version
    # def test_delete_homework_view_get(self):
    #     """Test delete homework confirmation page"""
    #     self.client.login(username="teacher", password="test123")
    #     response = self.client.get(reverse("delete_homework", kwargs={"pk": self.homework.pk}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "assignments/delete_homework.html")

    # def test_delete_homework_view_post(self):
    #     """Test deleting homework via POST"""
    #     self.client.login(username="teacher", password="test123")
    #     homework_pk = self.homework.pk
    #     response = self.client.post(reverse("delete_homework", kwargs={"pk": homework_pk}))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertFalse(Homework.objects.filter(pk=homework_pk).exists())

    def test_homework_submissions_view(self):
        """Test homework submissions view"""
        self.client.login(username="teacher", password="test123")
        file = SimpleUploadedFile("solution.txt", b"solution", content_type="text/plain")
        Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)

        response = self.client.get(reverse("teacher_homework_submissions", kwargs={"pk": self.homework.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/teacher_homework_submissions.html")
        self.assertEqual(len(response.context["submissions"]), 1)

    def test_grade_submission_view_get(self):
        """Test grade submission view displays form"""
        self.client.login(username="teacher", password="test123")
        file = SimpleUploadedFile("solution.txt", b"solution", content_type="text/plain")
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)

        response = self.client.get(reverse("teacher_grade_submission", kwargs={"pk": submission.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/teacher_grade_submission.html")

    def test_grade_submission_view_post(self):
        """Test grading submission via POST"""
        self.client.login(username="teacher", password="test123")
        file = SimpleUploadedFile("solution.txt", b"solution", content_type="text/plain")
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)

        form_data = {"grade": 95, "feedback": "Excellent work!"}
        response = self.client.post(reverse("teacher_grade_submission", kwargs={"pk": submission.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)
        submission.refresh_from_db()
        self.assertEqual(submission.grade, 95)
        self.assertEqual(submission.feedback, "Excellent work!")

    def test_all_submissions_view(self):
        """Test all submissions view"""
        self.client.login(username="teacher", password="test123")
        file = SimpleUploadedFile("solution.txt", b"solution", content_type="text/plain")
        Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)

        response = self.client.get(reverse("teacher_all_submissions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/teacher_all_submissions.html")
        self.assertIn("submissions", response.context)

    def test_all_submissions_filter_pending(self):
        """Test all submissions view filtering pending submissions"""
        self.client.login(username="teacher", password="test123")
        file = SimpleUploadedFile("solution.txt", b"solution", content_type="text/plain")
        Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)

        response = self.client.get(reverse("teacher_all_submissions") + "?status=pending")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["submissions"]), 1)

    def test_all_submissions_filter_graded(self):
        """Test all submissions view filtering graded submissions"""
        self.client.login(username="teacher", password="test123")
        file = SimpleUploadedFile("solution.txt", b"solution", content_type="text/plain")
        submission = Submission.objects.create(homework=self.homework, student=self.student, solution_file=file)
        submission.grade = 85
        submission.save()

        response = self.client.get(reverse("teacher_all_submissions") + "?status=graded")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["submissions"]), 1)


# ============================================================================
# DECORATOR TESTS
# ============================================================================


class DecoratorTest(TestCase):
    """Tests for custom decorators"""

    def setUp(self):
        """Set up test users"""
        self.client = Client()
        self.student = User.objects.create_user(username="student", password="test123")
        self.teacher = User.objects.create_user(username="teacher", password="test123")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

    def test_student_required_allows_students(self):
        """Test student_required decorator allows students"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_student_required_blocks_teachers(self):
        """Test student_required decorator blocks teachers"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_student_required_blocks_unauthenticated(self):
        """Test student_required decorator blocks unauthenticated users"""
        response = self.client.get(reverse("student_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_teacher_required_allows_teachers(self):
        """Test teacher_required decorator allows teachers"""
        self.client.login(username="teacher", password="test123")
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_teacher_required_blocks_students(self):
        """Test teacher_required decorator blocks students"""
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_teacher_required_blocks_unauthenticated(self):
        """Test teacher_required decorator blocks unauthenticated users"""
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 302)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class HomeworkWorkflowIntegrationTest(TestCase):
    """Integration tests for complete homework workflow"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.student = User.objects.create_user(username="student", password="test123", first_name="John", last_name="Doe")
        self.teacher = User.objects.create_user(username="teacher", password="test123", first_name="Jane", last_name="Smith")
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

    def test_complete_homework_workflow(self):
        """Test complete workflow: create homework, submit, grade"""
        # Teacher creates homework
        self.client.login(username="teacher", password="test123")

        # Create course first
        course = Course.objects.create(title="Integration Test Course", description="Test course")
        course.teachers.add(self.teacher)
        course.students.add(self.student)

        form_data = {
            "title": "Integration Test Homework",
            "description": "This is an integration test",
            "due_date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M"),
        }
        response = self.client.post(reverse("teacher_create_homework", kwargs={"course_pk": course.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)
        homework = Homework.objects.get(title="Integration Test Homework")

        # Student views homework and submits
        self.client.logout()
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("homework_detail", kwargs={"pk": homework.pk}))
        self.assertEqual(response.status_code, 200)

        file = SimpleUploadedFile("solution.txt", b"my solution", content_type="text/plain")
        response = self.client.post(reverse("homework_detail", kwargs={"pk": homework.pk}), {"solution_file": file})
        self.assertEqual(response.status_code, 302)

        # Check submission exists
        submission = Submission.objects.get(homework=homework, student=self.student)
        self.assertIsNotNone(submission)
        self.assertIsNone(submission.grade)

        # Teacher grades submission
        self.client.logout()
        self.client.login(username="teacher", password="test123")
        form_data = {"grade": 90, "feedback": "Great job!"}
        response = self.client.post(reverse("teacher_grade_submission", kwargs={"pk": submission.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)

        # Verify grade was saved
        submission.refresh_from_db()
        self.assertEqual(submission.grade, 90)
        self.assertEqual(submission.feedback, "Great job!")

        # Student can see grade
        self.client.logout()
        self.client.login(username="student", password="test123")
        response = self.client.get(reverse("my_submissions"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "90")

    def test_user_registration_and_login_workflow(self):
        """Test user can register, login, and access appropriate dashboard"""
        # Register as student
        form_data = {
            "username": "newstudent",
            "first_name": "New",
            "last_name": "Student",
            "email": "student@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "role": "student",
        }
        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(response.status_code, 302)

        # Check user was created and logged in
        user = User.objects.get(username="newstudent")
        self.assertEqual(user.profile.role, "student")

        # Access dashboard
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(reverse("student_dashboard")))


# ============================================================================
# SIGNAL TESTS
# ============================================================================


class SignalTest(TestCase):
    """Tests for model signals"""

    def test_user_profile_created_on_user_save(self):
        """Test that signal creates profile when user is created"""
        user = User.objects.create_user(username="testuser", password="test123")
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, UserProfile)

    def test_user_profile_saved_on_user_save(self):
        """Test that signal saves profile when user is saved"""
        user = User.objects.create_user(username="testuser", password="test123")
        user.profile.role = "teacher"
        user.profile.save()
        user.first_name = "Updated"
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.profile.role, "teacher")
