from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс модели пользователя"""

    is_student = models.BooleanField(default=False, verbose_name='Студент?')
    is_teacher = models.BooleanField(default=False, verbose_name='Преподаватель?')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username + ' ' + str(self.date_joined)


class Student(models.Model):
    """Класс модели студента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Пользователь')
    test = models.ManyToManyField("tasks.Test", verbose_name='Тесты')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    """Класс модели профиля"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ImageField(default='default.jpg', upload_to='profile', verbose_name='Изображение')
    completed_courses = models.ManyToManyField(
        "courses.Course",
        blank=True,
        verbose_name='Пройденные курсы'
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Token(models.Model):
    """Класс модели токена для сброса пароля"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    token = models.CharField(max_length=150, verbose_name='Токен')

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'
