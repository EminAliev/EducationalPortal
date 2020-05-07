from rest_framework import serializers

from courses.models import Subject, Course, Module


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['sort', 'name', 'definition']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'name', 'slug', 'view', 'date_created', 'followers', 'test_in_course',
                  'counter_tasks', 'user', 'modules']

