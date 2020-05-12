from django.contrib import admin

from users.models import User, Profile, Student, Token


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователей"""
    search_fields = ['username', 'first_name']
    list_display = ['username', 'is_active', 'is_student', 'is_teacher', 'first_name', 'last_name', 'email']
    date_hierarchy = 'date_joined'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админка профиля"""
    list_display = ['user', 'image']
    search_fields = ['user']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Админка студента"""
    list_display = ['user', ]
    search_fields = ['user']


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """Админка для токенов"""
    list_display = ['user', 'token']
