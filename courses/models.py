from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from courses.fields import SortField
from users.models import User


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
    user = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE, verbose_name='Предмет курса')
    name = models.CharField(max_length=250, verbose_name='Название курса')
    slug = models.SlugField(unique=True, verbose_name='Слаг курса')
    view = models.TextField(verbose_name='Описание курса')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания курса')
    followers = models.ManyToManyField(User, related_name='courses_joined', blank=True, verbose_name='Учащиеся курса')

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
    sort = SortField(blank=True, fields=['course'])

    class Meta:
        ordering = ['sort']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return '{}. {}'.format(self.sort, self.name)


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='content', on_delete=models.CASCADE,
                               verbose_name="Содержимое модуля")
    type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'text',
        'video',
        'image',
        'file')})
    obj_id = models.PositiveIntegerField()
    item = GenericForeignKey('type', 'obj_id')
    sort = SortField(blank=True, fields=['module'])

    class Meta:
        ordering = ['sort']
        verbose_name = 'Контент'


class AbstractContent(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AbstractItem(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE,
                             verbose_name="Пользователь")
    name = models.CharField(max_length=300, verbose_name="Название")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    data_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})


class Text(AbstractItem):
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = 'Текст'


class File(AbstractItem):
    file = models.FileField(upload_to='files', verbose_name="Файл")

    class Meta:
        verbose_name = 'Файлы'


class Image(AbstractItem):
    image = models.FileField(upload_to='images', verbose_name="Изображение")

    class Meta:
        verbose_name = 'Изображения'


class Video(AbstractItem):
    path = models.URLField(verbose_name="Ссылка")

    class Meta:
        verbose_name = 'Видео'
