from django.contrib import admin
from django.utils.safestring import mark_safe

from courses.models import Course, Module, Subject, Content, Task, MessagesTask, TaskRealization


def all_fields_admin(cls, *exclude_fields):
    """Забирает все поля для list_display"""
    return [field.name for field in cls._meta.fields if field.name not in exclude_fields]


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка курсов"""
    list_display = ['name', 'subject', 'date_created']
    search_fields = ['name', 'view']
    list_filter = ['date_created', 'subject']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Админка предметов"""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class TaskAdmin(admin.ModelAdmin):
    """Админка заданий"""
    list_display = all_fields_admin(Task, 'id', 'description')
    list_display_links = ("name",)
    actions = ['show_task']

    def show_task(self, request, queryset):
        queryset.update(active=True)

    show_task.short_description = "Вывести задание"


class RealizationTaskAdmin(admin.ModelAdmin):
    """Админка выполнения заданий"""

    class MessagesTaskAdmin(admin.TabularInline):
        """Добавления вопросов при создании теста"""
        model = MessagesTask

    inlines = [
        MessagesTaskAdmin,
    ]

    list_display = ("id", "student", "task", "success", "date_create")
    list_filter = ("task__name", "student__username", "date_create")
    list_editable = ("success",)
    readonly_fields = ('answer',)
    list_display_links = ("student",)

    def answer(self, obj):
        return mark_safe("{}|safe".format(obj.answer))


class MessagesTaskAdmin(admin.ModelAdmin):
    """Админка для комментариев в задании"""
    list_display = ("user", "task_realization", "date_created")


admin.site.register(Content)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskRealization, RealizationTaskAdmin)
admin.site.register(MessagesTask, MessagesTaskAdmin)
