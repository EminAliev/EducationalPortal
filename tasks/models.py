from django.db import models

from courses.models import Course
from users.models import User


class Test(models.Model):
    """Класс модели тестов"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test')
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='test')

    def __str__(self):
        return self.name


class Question(models.Model):
    """Класс модели вопрос"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField('Вопрос')

    def __str__(self):
        return self.question


class Answer(models.Model):
    """Класс модели ответов"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField('Ответ')
    correct_answer = models.BooleanField('Правильный ответ', default=False)

    def __str__(self):
        return self.answer


class Student(models.Model):
    """Класс модели студента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    test = models.ManyToManyField(Test)

    def __str__(self):
        return self.user.username


class CompleteTest(models.Model):
    """Класс модели выполенный тест"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complete_test')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='complete_test')
    result = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)


class StudentAnswerTest(models.Model):
    """Класс модели ответа студента"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer')
