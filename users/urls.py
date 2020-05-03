from django.urls import path

from users.views import login_view, logout_view, register, UserEntryToCourseView, UserCourseView, UserCourseInView

urlpatterns = [
    path('signIn/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signUp/', register, name='register'),
    path('entry-course/', UserEntryToCourseView.as_view(), name='users_entry_course'),
    path('courses/', UserCourseView.as_view(), name='users_list_courses'),
    path('course/<pk>/', UserCourseInView.as_view(), name='users_course_in'),
    path('course/<pk>/<module_id>/', UserCourseInView.as_view(), name='users_course_in_module'),
]
