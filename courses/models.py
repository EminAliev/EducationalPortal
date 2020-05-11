from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from courses.fields import SortField
from tasks.models import Test
from users.models import User


class Subject(models.Model):
    """Класс модели предмета"""
    name = models.CharField(max_length=250, verbose_name='Название предмета')
    slug = models.SlugField(unique=True, verbose_name='Слаг предмета')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """Класс модели курса"""
    user = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE, verbose_name='Предмет курса')
    name = models.CharField(max_length=250, verbose_name='Название курса')
    slug = models.SlugField(unique=True, verbose_name='Слаг курса')
    view = models.TextField(verbose_name='Описание курса')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания курса')
    followers = models.ManyToManyField(User, related_name='courses_joined', blank=True, verbose_name='Учащиеся курса')
    counter_tasks = models.PositiveIntegerField('Количество заданий', default=0)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-date_created']

    def __str__(self):
        return self.name


class Module(models.Model):
    """Класс модели модуль"""
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
    """Класс модели контента(содержимого в модулях)"""
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
        verbose_name_plural = 'Контенты'


class AbstractContent(models.Model):
    """Абстрактный класс модели контента"""
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AbstractItem(models.Model):
    """Абстрактный класс модели видов контента(содержимого)"""
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
    """Класс модели текста"""
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = 'Текст'


class File(AbstractItem):
    """Класс модели файла"""
    file = models.FileField(upload_to='files', verbose_name="Файл")

    class Meta:
        verbose_name = 'Файлы'


class Image(AbstractItem):
    """Класс модели изображения"""
    image = models.FileField(upload_to='images', verbose_name="Изображение")

    class Meta:
        verbose_name = 'Изображения'


class Video(AbstractItem):
    """Класс модели видео"""
    path = models.URLField(verbose_name="Ссылка")

    class Meta:
        verbose_name = 'Видео'


class Comment(models.Model):
    """Класс модели комментариев"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='comments_course')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')

    class Meta:
        ordering = ('created',)
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.course)


class Contact(models.Model):
    """Класс модели подписки по email"""
    name = models.CharField(max_length=30, verbose_name='Имя')
    email = models.CharField(max_length=50, verbose_name='Email')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.name
