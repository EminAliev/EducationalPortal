from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View

from tasks.models import Test


"""class TestView(ListView):
    queryset = Test.objects.filter(active=True, for_course=False, course__test_in_course__isnull=True)
    template_name = "tasks/list.html

    def get(self, request):
        tasks = Test.objects.all()
        return render(request, "tasks/list.html", {"object_list": tasks})"""
