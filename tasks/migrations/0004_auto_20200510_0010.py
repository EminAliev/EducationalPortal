# Generated by Django 2.0.5 on 2020-05-10 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200509_2322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentanswertest',
            old_name='answer',
            new_name='answer_text',
        ),
    ]
