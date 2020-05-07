from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(ModelAdmin):
    """Админка пользователей"""
    search_fields = [
        'username',
    ]
    list_display = [
        'username',
        'is_active',
    ]

    date_hierarchy = 'date_joined'


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    """Админка профиля"""
    list_display = ['user', 'image']
