# Generated by Django 2.0.5 on 2020-04-23 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20200423_1556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-date_created'], 'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'verbose_name': 'Модуль', 'verbose_name_plural': 'Модули'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name'], 'verbose_name': 'Предмет', 'verbose_name_plural': 'Предметы'},
        ),
    ]