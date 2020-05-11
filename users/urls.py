from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from users.views import login_view, logout_view, UserEntryToCourseView, UserCourseView, UserCourseInView, \
    edit, ProfileView, RegisterView, StudentRegister, TeacherRegister

urlpatterns = [
    path('signIn/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signUp/', RegisterView.as_view(), name='register'),
    path('signUp/student/', StudentRegister.as_view(), name='register_student'),
    path('signUp/teacher/', TeacherRegister.as_view(), name='register_teacher'),
    path('reset/', PasswordResetView.as_view(template_name='users/auth/reset.html'), name='reset'),
    path('reset/ready/', PasswordResetDoneView.as_view(template_name='users/auth/ready.html'), name='ready'),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/auth/confirm.html'),
         name='confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(template_name='users/auth/complete.html'),
         name='complete'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('edit/', edit, name='edit'),
    path('entry-course/', UserEntryToCourseView.as_view(), name='users_entry_course'),
    path('courses/', UserCourseView.as_view(), name='users_list_courses'),
    path('course/<pk>/', UserCourseInView.as_view(), name='users_course_in'),
    path('course/<pk>/<module_id>/', UserCourseInView.as_view(), name='users_course_in_module'),
]
