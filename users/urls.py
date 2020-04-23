from django.urls import path

from users.views import login_view, logout_view, register

urlpatterns = [
    path('signIn/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signUp/', register, name='register'),
]
