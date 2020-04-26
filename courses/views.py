from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from courses.models import Course


class UserMixin(object):
    def get_queryset(self):
        queryset = super(UserMixin, self).get_queryset()
        return queryset.filter(user=self.request.user)


class UserEditMixin(object):
    def validate(self, form):
        form.instance.user = self.request.user
        return super(UserEditMixin, self).validate(form)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'name', 'slug', 'view']
    success_url = reverse_lazy('course_list')


class UserCourseEditMixin(UserCourseMixin, UserEditMixin):
    fields = ['subject', 'name', 'slug', 'view']
    success_url = reverse_lazy('course_list')
    template_name = ''


class CourseView(UserCourseMixin, ListView):
    template_name = 'courses/list_courses.html'


class CourseCreateView(PermissionRequiredMixin, UserCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    template_name = 'courses/create_course.html'


class CourseUpdateView(PermissionRequiredMixin, UserCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'
    template_name = 'courses/create_course.html'


class CourseDeleteView(PermissionRequiredMixin, UserCourseMixin, DeleteView):
    template_name = "courses/delete_course.html"
    success_url = reverse_lazy('course_list')
    permission_required = 'courses.delete_course'
