from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.courses.serializers import SubjectSerializer
from courses.models import Subject, Course


class SubjectView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectInView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class EntryToCourseView(APIView):

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.followers.add(request.user)
        return Response({'entry': True})
