from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView

from courses.models import Course
from users.forms import LoginForm, RegisterForm, CourseForm
from users.models import User


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/course')
            else:
                return render(
                    request, "users/signIn.html",
                    {"form": form, "errors": ["Incorrect login or password"]})
        else:
            return render(request, "users/signIn.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "users/signIn.html", {"form": form})


@login_required(login_url="/auth/signIn")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/auth/signIn")


def register(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"])

            return redirect(reverse("login"))
        else:
            return render(request, "users/signUp.html", {"form": form})
    else:
        return render(request, "users/signUp.html", {"form": RegisterForm()})


class UserEntryToCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.followers.add(self.request.user)
        return super(UserEntryToCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users_course_in', args=[self.course.id])


class UserCourseView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'users/list_courses.html'

    def get_queryset(self):
        queryset = super(UserCourseView, self).get_queryset()
        return queryset.filter(followers__in=[self.request.user])


class UserCourseInView(DetailView):
    model = Course
    template_name = 'users/course_in.html'

    def get_queryset(self):
        queryset = super(UserCourseInView, self).get_queryset()
        return queryset.filter(followers__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(UserCourseInView, self).get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]
        return context
