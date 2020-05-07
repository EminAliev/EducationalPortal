from rest_framework import serializers

from courses.models import Subject, Course, Module, Content


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


class Item(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = Item(read_only=True)

    class Meta:
        model = Content
        fields = ['sort', 'item']


class ContentModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['sort', 'name', 'definition', 'contents']


class ContentCourseSerializer(serializers.ModelSerializer):
    content_modules = ContentModuleSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'name', 'slug', 'view', 'date_created', 'followers', 'test_in_course',
                  'counter_tasks', 'user', 'content_modules']
