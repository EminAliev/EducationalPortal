from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import LoginForm, RegisterForm
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
                return HttpResponseRedirect('/course/list')
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
