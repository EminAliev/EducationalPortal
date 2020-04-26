from django.urls import path
from . import views

urlpatterns = [
    path('list/',
         views.CourseView.as_view(),
         name='course_list'),
    path('create/',
         views.CourseCreateView.as_view(),
         name='course_create'),
    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),
    path(r'^(?P<pk>\d+)/delete/$',
         views.CourseDeleteView.as_view(),
         name='course_delete'),
]
