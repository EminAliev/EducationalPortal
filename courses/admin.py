from django.contrib import admin

from courses.models import Course, Module, Subject


class ModuleInline(object):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created']
    search_fields = ['name', 'view']
    list_filter = ['data_created', 'subject']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
