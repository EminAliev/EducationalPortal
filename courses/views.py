from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View

from courses.forms import CourseModuleFormSet
from courses.models import Course


class UserMixin(object):
    def get_queryset(self):
        queryset = super(UserMixin, self).get_queryset()
        return queryset.filter(user=self.request.user)


class UserEditMixin(object):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserEditMixin, self).form_valid(form)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'name', 'slug', 'view']
    success_url = reverse_lazy('course_list')


class UserCourseEditMixin(UserCourseMixin, UserEditMixin):
    fields = ['subject', 'name', 'slug', 'view']
    success_url = reverse_lazy('course_list')
    template_name = 'courses/create_course.html'


class CourseView(UserCourseMixin, ListView):
    template_name = 'courses/list_courses.html'


class CourseCreateView(PermissionRequiredMixin, UserCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, UserCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, UserCourseMixin, DeleteView):
    template_name = "courses/delete_course.html"
    success_url = reverse_lazy('course_list')
    permission_required = 'courses.delete_course'


class ModuleCourseCreateUpdateView(TemplateResponseMixin, View):
    template_name = "courses/update_create_module.html"
    course = None

    def get_formset(self, data=None):
        return CourseModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, user=request.user)
        return super(ModuleCourseCreateUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})
