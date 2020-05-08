"""EducationalPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from api.courses import views
from .yasg import urlpatterns as doc_urls

from api.courses.views import SubjectView, SubjectInView, CourseView

router = routers.DefaultRouter()
router.register('courses', CourseView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('course/', include('courses.urls')),
    path('test/', include('tasks.urls')),
    path('', TemplateView.as_view(template_name="index.html"), name='index'),

    # REST API
    path('api/subjects/', SubjectView.as_view(), name='subjects_all'),
    path('api/subjects/<pk>/', SubjectInView.as_view(), name='subject_in'),
    path('api/', include(router.urls)),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
