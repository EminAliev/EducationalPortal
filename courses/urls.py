from django.urls import path
from . import views
from .views import CourseView, CourseCreateView, CourseUpdateView, CourseDeleteView, ModuleCourseCreateUpdateView, \
    ContentCreateView, ContentCancelView

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
         name='module_course_update_create'),
    path('module/<int:module_id>/content/<model_in>/new/',
         ContentCreateView.as_view(),
         name='module_create'),
    path('module/<int:module_id>/content/<model_in>/<id>/',
         ContentCreateView.as_view(),
         name='module_change'),
    path('content/<int:id>/cancel/',
         ContentCancelView.as_view(),
         name='module_delete'),
]
