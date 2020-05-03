from django.contrib import admin

from courses.models import Course, Module, Subject, Content


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'date_created']
    search_fields = ['name', 'view']
    list_filter = ['date_created', 'subject']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Content)
