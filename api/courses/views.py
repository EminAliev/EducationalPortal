from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from api.courses.serializers import SubjectSerializer, CourseSerializer, ContentCourseSerializer
from courses.models import Subject, Course


class SubjectView(ListAPIView):
    """Список предметов"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectInView(RetrieveAPIView):
    """Подробное описание предмета"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class EntryToCourse(BasePermission):
    """Доступ к содержимого курсов"""

    def has_object_permission(self, request, view, obj):
        return obj.followers.filter(id=request.user.id).exists()


class CourseView(ReadOnlyModelViewSet):
    """Просмотр курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['post'],
            detail=True,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def entry(self, request, *args, **kwargs):
        """Зачисление учеников на курс"""
        course = self.get_object()
        course.followers.add(request.user)
        return Response({'entry': True})

    @action(methods=['get'],
            detail=True,
            serializer_class=ContentCourseSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, EntryToCourse])
    def contents_courses(self, request, *args, **kwargs):
        """Возвращает данные курса, его модулей и контента(содержимого)"""
        return self.retrieve(request, *args, **kwargs)
