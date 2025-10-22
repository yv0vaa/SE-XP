from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Homework, Submission, UserProfile


class RegisterForm(UserCreationForm):
    """Форма регистрации с выбором роли"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=True,
        label='Роль',
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Русификация полей
        self.fields['username'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        # Добавляем Bootstrap классы
        for field_name, field in self.fields.items():
            if field_name != 'role':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Устанавливаем роль в профиле
            user.profile.role = self.cleaned_data['role']
            user.profile.save()

        return user


class HomeworkForm(forms.ModelForm):
    """Форма создания домашнего задания"""

    class Meta:
        model = Homework
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задания'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Опишите задание подробно'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'title': 'Название задания',
            'description': 'Описание',
            'due_date': 'Срок сдачи',
        }


class SubmissionForm(forms.ModelForm):
    """Форма отправки работы студентом"""

    class Meta:
        model = Submission
        fields = ['solution_file']
        widgets = {
            'solution_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt,.py,.zip'
            }),
        }
        labels = {
            'solution_file': 'Файл с решением',
        }


class GradeForm(forms.ModelForm):
    """Форма для выставления оценки и отзыва"""

    class Meta:
        model = Submission
        fields = ['grade', 'feedback']
        widgets = {
            'grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'placeholder': 'Оценка от 0 до 100'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите отзыв о работе'
            }),
        }
        labels = {
            'grade': 'Оценка',
            'feedback': 'Отзыв',
        }
