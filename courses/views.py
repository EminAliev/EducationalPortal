from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View

from courses.forms import CourseModuleFormSet
from courses.models import Course, Module, Content


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


class ContentCreateView(TemplateResponseMixin, View):
    module = None
    model = None
    object = None
    template_name = 'courses/module_create_files.html'

    def get_model(self, model_in):
        if model_in in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_in)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['user', 'sort', 'date_created', 'data_updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_in, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__user=request.user)
        self.model = self.get_model(model_in)
        if id:
            self.object = get_object_or_404(self.model, id=id, user=request.user)
        return super(ContentCreateView, self).dispatch(request, module_id, model_in, id)

    def get(self, request, module_id, model_in, id=None):
        content_form = self.get_form(self.model, instance=self.object)
        return self.render_to_response({'form': content_form, 'object': self.object})

    def post(self, request, module_id, model_in, id=None):
        form = self.get_form(self.model, instance=self.object, data=request.POST, files=request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.save()
            if not id:
                Content.objects.create(module=self.module, item=object)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.object})


class ContentCancelView(View):

    def post(self, request, id):
        content_object = get_object_or_404(Content, id=id, module__course__user=request.user)
        module_object = content_object.module
        content_object.item.delete()
        content_object.delete()
        return redirect('module_content_list', module_object.id)
