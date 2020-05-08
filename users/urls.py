from django.urls import path

from users.views import login_view, logout_view, UserEntryToCourseView, UserCourseView, UserCourseInView, \
    edit, ProfileView, RegisterView, StudentRegister, TeacherRegister

urlpatterns = [
    path('signIn/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signUp/', RegisterView.as_view(), name='register'),
    path('signUp/student/', StudentRegister.as_view(), name='register_student'),
    path('signUp/teacher/', TeacherRegister.as_view(), name='register_teacher'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('edit/', edit, name='edit'),
    path('entry-course/', UserEntryToCourseView.as_view(), name='users_entry_course'),
    path('courses/', UserCourseView.as_view(), name='users_list_courses'),
    path('course/<pk>/', UserCourseInView.as_view(), name='users_course_in'),
    path('course/<pk>/<module_id>/', UserCourseInView.as_view(), name='users_course_in_module'),
]
