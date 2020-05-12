from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from users.views import login_view, logout_view, UserEntryToCourseView, UserCourseView, UserCourseInView, \
    edit, ProfileView, RegisterView, StudentRegister, TeacherRegister, ResetPasswordRequestView, ResetPasswordView, \
    CheckEmailView

urlpatterns = [
    path('signIn/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signUp/', RegisterView.as_view(), name='register'),
    path('signUp/student/', StudentRegister.as_view(), name='register_student'),
    path('signUp/teacher/', TeacherRegister.as_view(), name='register_teacher'),
    path('reset/', ResetPasswordRequestView.as_view(), name='reset_request_user'),
    path('reset/<username>/<token>', ResetPasswordView.as_view(), name='reset'),
    path('reset/ready/', CheckEmailView.as_view(), name='check_email'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('edit/', edit, name='edit'),
    path('entry-course/', UserEntryToCourseView.as_view(), name='users_entry_course'),
    path('courses/', UserCourseView.as_view(), name='users_list_courses'),
    path('course/<pk>/', UserCourseInView.as_view(), name='users_course_in'),
    path('course/<pk>/<module_id>/', UserCourseInView.as_view(), name='users_course_in_module'),
]
