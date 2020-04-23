from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    search_fields = [
        'username',
    ]
    list_display = [
        'username',
        'is_active',
    ]

    date_hierarchy = 'date_joined'
