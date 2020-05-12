from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import CharField, PasswordInput

from courses.models import Course
from users.models import User, Profile, Student


class StudentRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TeacherRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(TeacherRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Форма для авторизации"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileEditForm(forms.ModelForm):
    """Форма для изменении профиля"""

    class Meta:
        model = Profile
        fields = ('image',)


class UserEditForm(forms.ModelForm):
    """Форма для изменения данных"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CourseForm(forms.Form):
    """Форма для записи на курс"""
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("email"), max_length=254)


class PasswordResetForm(forms.Form):
    password = CharField(label="New Password", max_length=254, widget=PasswordInput())
