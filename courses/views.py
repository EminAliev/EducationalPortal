from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin, View

from courses.forms import CourseModuleFormSet
from courses.models import Course, Module, Content, Subject


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
    template_name = 'courses/control/list_courses.html'


class CourseCreateView(PermissionRequiredMixin, UserCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, UserCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, UserCourseMixin, DeleteView):
    template_name = "courses/control/delete_course.html"
    success_url = reverse_lazy('course_list')
    permission_required = 'courses.delete_course'


class ModuleCourseCreateUpdateView(TemplateResponseMixin, View):
    template_name = "courses/control/update_create_module.html"
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


class ContentViewCreate(TemplateResponseMixin, View):
    module = None
    model = None
    obj_item = None
    template_name = 'courses/control/module_create_files.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['user', 'sort', 'date_created', 'data_updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__user=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj_item = get_object_or_404(self.model, id=id, user=request.user)
        return super(ContentViewCreate, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj_item)
        return self.render_to_response({'form': form, 'object': self.obj_item})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj_item, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj_item = form.save(commit=False)
            obj_item.user = request.user
            obj_item.save()
            if not id:
                Content.objects.create(module=self.module, item=obj_item)
            return redirect('content_view', self.module.id)

        return self.render_to_response({'form': form, 'object': self.obj_item})


class ContentCancelView(View):

    def post(self, request, id):
        content_object = get_object_or_404(Content, id=id, module__course__user=request.user)
        module_object = content_object.module
        content_object.item.delete()
        content_object.delete()
        return redirect('content_view', module_object.id)


class ContentListView(TemplateResponseMixin, View):
    template_name = 'courses/control/content_view.html'

    def get(self, request, module_id):
        module_object = get_object_or_404(Module, id=module_id, course__user=request.user)
        return self.render_to_response({'module': module_object})


class SortViewForModules(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, sort in self.request_json.items():
            Module.objects.filter(id=id, course__user=request.user).update(sort=sort)
        return self.render_json_response({'saved': 'OK'})


class SortViewForContent(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, sort in self.request_json.items():
            Content.objects.filter(id=id, module__course__user=request.user).update(sort=sort)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/courses_all.html'

    def get(self, request, subject=None):
        subjects_objects = Subject.objects.annotate(total_courses=Count('courses'))
        courses_objects = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
        courses_objects = courses_objects.filter(subject=subject)
        return self.render_to_response(
            {'subjects_objects': subjects_objects, 'subject': subject, 'courses_objects': courses_objects})


class CourseInView(DetailView):
    model = Course
    template_name = 'courses/courses_all_in.html'
