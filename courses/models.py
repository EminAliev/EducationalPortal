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
    test_in_course = models.ForeignKey(Test, verbose_name="Тест", on_delete=models.SET_NULL, blank=True,
                                       null=True)
    counter_tasks = models.PositiveIntegerField('Количество заданий', default=0)

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


class Task(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField('Название задания', max_length=50)
    description = models.TextField('Описание задания')
    date_start = models.DateTimeField('Дата начала выполнения задания')
    date_end = models.DateTimeField('Дата окончания выполнения задания')
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тест',
                             related_name='tasks')
    active = models.BooleanField("Вывести задание", default=False)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ["name"]

    def __str__(self):
        return self.name


@receiver(post_save, sender=Task)
def plus_count_tasks(instance, created, **kwargs):
    """Прибавление 1 к счетчику заданий в курсе"""
    if created:
        instance.course.counter_tasks += 1
        instance.course.save()


@receiver(post_delete, sender=Task)
def minus_count_tasks(instance, **kwargs):
    """Убавление 1 от счетчика заданий в курсе"""
    instance.course.counter_tasks -= 1
    instance.course.save()


class TaskRealization(models.Model):
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE)
    answer = models.TextField('Ответ')
    comment = models.TextField('Комментарий преподавателя', blank=True)
    success = models.BooleanField('Выполнено', default=False)
    date_create = models.DateTimeField('Дата сдачи', auto_now_add=True)

    def __str__(self):
        return self.task.name

    def add_complete(self):
        realizations_count = TaskRealization.objects.filter(student=self.student).count()
        tasks_count = self.task.course.counter_tasks
        if realizations_count == tasks_count:
            self.student.profile.completed_courses.add(self.task.course)

    def save(self, *args, **kwargs):
        self.add_complete()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Выполненное задание'
        verbose_name_plural = 'Выполненные задания'


class MessagesTask(models.Model):
    task_realization = models.ForeignKey(TaskRealization, verbose_name='Выполнение', on_delete=models.CASCADE,
                                         related_name='realization_task')
    user = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE)
    answer = models.TextField('Сообщение')
    date_created = models.DateTimeField("Дата", auto_now_add=True)
    read = models.BooleanField("Просмотренно", default=False)

    def __str__(self):
        return "{}".format(self.task_realization)

    class Meta:
        verbose_name = "Сообщение в задании"
        verbose_name_plural = "Сообщения в задании"
