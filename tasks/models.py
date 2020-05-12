from django.db import models

from users.models import User, Student


class Test(models.Model):
    """Класс модели тестов"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test', verbose_name='Автор')
    name = models.CharField(max_length=255, verbose_name='Название теста')
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name='test', verbose_name='Курс')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name


class Question(models.Model):
    """Класс модели вопрос"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    question_text = models.TextField(verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    """Класс модели ответов"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    correct_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.answer


class CompleteTest(models.Model):
    """Класс модели выполенный тест"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complete_test', verbose_name='Студент')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='complete_test', verbose_name='Тест')
    result = models.FloatField(verbose_name='Результат')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Выполненный тест'
        verbose_name_plural = 'Выполненные тесты'


class StudentAnswerTest(models.Model):
    """Класс модели ответа студента"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tests_answers', verbose_name='Студент')
    answer_text = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_student',
                                    verbose_name='Ответ студента')

    class Meta:
        verbose_name = 'Результат студента'
        verbose_name_plural = 'Результаты студента'
