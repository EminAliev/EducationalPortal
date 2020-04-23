from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)


class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    view = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    definition = models.TextField(blank=True)
