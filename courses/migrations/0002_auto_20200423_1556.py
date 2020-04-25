# Generated by Django 2.0.5 on 2020-04-23 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Слаг курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.Subject', verbose_name='Предмет курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='view',
            field=models.TextField(verbose_name='Описание курса'),
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.Course', verbose_name='Курс модуля'),
        ),
        migrations.AlterField(
            model_name='module',
            name='definition',
            field=models.TextField(blank=True, verbose_name='Описание модуля'),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название модуля'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название предмета'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Слаг предмета'),
        ),
    ]