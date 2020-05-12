from django.contrib import admin

from courses.models import Course, Module, Subject, Content, Contact, Comment


class ModuleInline(admin.StackedInline):
    model = Module


class ContentInline(admin.StackedInline):
    model = Content


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка курсов"""
    list_display = ['name', 'subject', 'date_created']
    search_fields = ['name', 'view']
    list_filter = ['date_created', 'subject']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline, CommentInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Админка предметов"""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Админка модулей"""
    list_display = ['course', 'name', 'definition']
    search_fields = ['name']
    list_filter = ['course']
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Админка содержимого"""
    list_display = ['module', 'type']
    search_fields = ['type']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка отзывов(комментариев)"""
    list_display = ['course', 'user', 'text', 'created']
    search_fields = ['text', 'created']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Админка подписки"""
    list_display = ('name', 'email')
