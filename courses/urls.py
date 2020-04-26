from django.urls import path
from . import views
from .views import CourseView, CourseCreateView, CourseUpdateView, CourseDeleteView, ModuleCourseCreateUpdateView

urlpatterns = [
    path('list/',
         CourseView.as_view(),
         name='course_list'),
    path('create/',
         CourseCreateView.as_view(),
         name='course_create'),
    path('<pk>/edit/',
         CourseUpdateView.as_view(),
         name='course_edit'),
    path(r'^(?P<pk>\d+)/delete/$',
         CourseDeleteView.as_view(),
         name='course_delete'),
    path('<pk>/module/',
         ModuleCourseCreateUpdateView.as_view(),
         name='module_course_update_create')
]
