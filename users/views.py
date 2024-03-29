from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, TemplateView

from courses.models import Course
from users.forms import LoginForm, CourseForm, ProfileEditForm, UserEditForm, StudentRegisterForm, \
    TeacherRegisterForm, PasswordResetRequestForm, PasswordResetForm
from users.models import User, Profile, Token
from users.tasks import send_email_password


def teacher_required(f):
    @wraps(f)
    def g(request, *args, **kwargs):
        if request.user.is_student:
            raise PermissionDenied
        else:
            return f(request, *args, **kwargs)

    return g


def student_required(f):
    @wraps(f)
    def g(request, *args, **kwargs):
        if request.user.is_teacher:
            raise PermissionDenied
        else:
            return f(request, *args, **kwargs)

    return g


class StudentRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_teacher:
            raise PermissionDenied
        return super(StudentRequiredMixin, self).dispatch(request, *args, **kwargs)


class TeacherRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_student:
            raise PermissionDenied
        return super(TeacherRequiredMixin, self).dispatch(request, *args, **kwargs)


def login_view(request):
    """Авторизация пользователя"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect('courses_all')
            else:
                return render(
                    request, "users/auth/signIn.html",
                    {"form": form, "errors": ["Incorrect login or password"]})
        else:
            return render(request, "users/auth/signIn.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "users/auth/signIn.html", {"form": form})


class RegisterView(TemplateView):
    """Отображение страницы регистрации"""
    template_name = 'users/auth/signUp_base.html'


@login_required(login_url="/auth/signIn")
def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('index')


class StudentRegister(CreateView):
    """Регистрация студента"""
    model = User
    form_class = StudentRegisterForm
    template_name = 'users/auth/signUp.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('index')


class TeacherRegister(CreateView):
    """Регистрация учителя"""
    model = User
    form_class = TeacherRegisterForm
    template_name = 'users/auth/signUp.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('index')


class ProfileView(LoginRequiredMixin, DetailView):
    """Просмотр профиль пользователя"""
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/auth/profile.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Profile, user=self.request.user)
        if obj.user != self.request.user:
            raise Http404
        return obj


@login_required
def edit(request):
    """Изменение данных в профиле"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'users/auth/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


class UserEntryToCourseView(LoginRequiredMixin, FormView):
    """Запись на курс"""
    course = None
    form_class = CourseForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.followers.add(self.request.user)
        return super(UserEntryToCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users_course_in', args=[self.course.id])


class UserCourseView(LoginRequiredMixin, ListView):
    """Просмотр курсов текущего пользователя"""
    model = Course
    template_name = 'users/list_courses.html'

    def get_queryset(self):
        queryset = super(UserCourseView, self).get_queryset()
        return queryset.filter(followers__in=[self.request.user])


class UserCourseInView(DetailView):
    """Просмотр детального описания курса текущего пользователя"""
    model = Course
    template_name = 'users/course_in.html'

    def get_queryset(self):
        queryset = super(UserCourseInView, self).get_queryset()
        return queryset.filter(followers__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(UserCourseInView, self).get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # Получаем текущий модуль
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # Получаем первый модуль
            context['module'] = course.modules.all()[0]
        return context


class ResetPasswordRequestView(FormView):
    """Запрос для сброса пароля(формирование ссылки)"""
    template_name = 'users/auth/reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('check_email')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            user = User.objects.get(email=data)
            new_token = default_token_generator.make_token(user)
            Token.objects.create(user=user, token=new_token)
            link = str('http://localhost:8000') + reverse('reset',
                                                          kwargs={'username': user.username, 'token': new_token})
            send_email_password.delay('Пройдите по ссылке, чтобы создать новый пароль: ' + link, user.email)
        return self.form_valid(form)


class UserResetPasswordAccessMixin(AccessMixin):
    """Обработка ссылки для сброса пароля"""

    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        user = User.objects.get(username=username)
        token = kwargs['token']
        try:
            Token.objects.get(user=user, token=token)
        except Token.DoesNotExist:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ResetPasswordView(UserResetPasswordAccessMixin, FormView):
    """Создание нового пароля"""
    form_class = PasswordResetForm
    template_name = 'users/auth/confirm.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["password"]
            username = kwargs['username']
            token = kwargs['token']
            token_on_user = Token.objects.get(user__username=username, token=token)
            user = token_on_user.user
            user.set_password(data)
            user.save()
            token_on_user.delete()
        return self.form_valid(form)


class CheckEmailView(TemplateView):
    """Отображение инструкции для сброса пароля"""
    template_name = 'users/auth/ready.html'
