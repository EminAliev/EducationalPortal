# Generated by Django 2.0.5 on 2020-05-13 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200513_0858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='counter_tasks',
        ),
    ]
