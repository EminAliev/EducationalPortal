from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название предмета')
    slug = models.SlugField(unique=True, verbose_name='Слаг предмета')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE, verbose_name='Предмет курса')
    name = models.CharField(max_length=250, verbose_name='Название курса')
    slug = models.SlugField(unique=True, verbose_name='Слаг курса')
    view = models.TextField(verbose_name='Описание курса')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-date_created']

    def __str__(self):
        return self.name


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс модуля')
    name = models.CharField(max_length=250, verbose_name='Название модуля')
    definition = models.TextField(blank=True, verbose_name='Описание модуля')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.name


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE,
                               verbose_name="Содержимое модуля")
    type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    obj_id = models.PositiveIntegerField()
    item = GenericForeignKey('type', 'obj_id')


class AbstractContent(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Text(AbstractContent):
    words = models.TextField(verbose_name="Текст")


class SortingContent(AbstractContent):
    class Meta:
        proxy = True
        ordering = ['date_created']

    def time(self):
        return timezone.now() - self.date_created
