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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    test = models.ManyToManyField("tasks.Test")

    def __str__(self):
        return self.user.username

    def get_not_completed_questions(self, test):
        answers = self.tests_answers.filter(answer_text__question__test=test).values_list(
            'answer_text__question__test_id',
            flat=True)
        questions = test.questions.exclude(pk__in=answers).order_by('question_text')
        print(questions)
        return questions


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

