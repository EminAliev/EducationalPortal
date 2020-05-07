from django import forms

from courses.models import Course
from users.models import User, Profile


class LoginForm(forms.Form):
    """Форма для авторизации"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    """Форма для регистрации"""
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {"username", "email", "password"}


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
