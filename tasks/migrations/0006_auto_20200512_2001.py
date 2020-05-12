# Generated by Django 2.0.5 on 2020-05-12 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20200512_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tasks.Question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='completetest',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='completetest',
            name='result',
            field=models.FloatField(verbose_name='Результат'),
        ),
        migrations.AlterField(
            model_name='completetest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complete_test', to='users.Student', verbose_name='Студент'),
        ),
        migrations.AlterField(
            model_name='completetest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complete_test', to='tasks.Test', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tasks.Test', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='studentanswertest',
            name='answer_text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_student', to='tasks.Answer', verbose_name='Ответ студента'),
        ),
        migrations.AlterField(
            model_name='studentanswertest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_answers', to='users.Student', verbose_name='Студент'),
        ),
        migrations.AlterField(
            model_name='test',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='test',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='courses.Course', verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название теста'),
        ),
    ]