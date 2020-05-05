from django.db import models

from users.models import User


class TestSubject(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест предмета'
        verbose_name_plural = 'Тесты предмета'


class Test(models.Model):
    test_subject = models.ForeignKey(TestSubject, on_delete=models.SET_NULL,
                                     related_name='tests',
                                     verbose_name='Тест предмета',
                                     null=True,
                                     blank=True)

    name = models.CharField('Название', max_length=200)
    active = models.BooleanField('Активный', default=1)
    for_course = models.BooleanField('Для курса', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест'
    )
    question = models.TextField('Вопрос')
    description = models.TextField("Описание вопроса", default="")

    def __str__(self):
        return '{} - {}'.format(self.test, self.question)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    answer = models.TextField('Вариант')
    right = models.BooleanField('Является верным ответом', default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class CounterAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers_counter',
        verbose_name='Пользователь'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='counter',
        verbose_name='Тест'
    )

    count_question = models.PositiveIntegerField(default=0, editable=False)
    counter = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Ответ на тест"
        verbose_name_plural = "Ответы на тесты"

    def save(self, *args, **kwargs):
        self.questions_count = self.test.questions.all().count()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.user, self.test)
