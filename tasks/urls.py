from django.urls import path

from tasks.views import TestView, TestChange, TestDelete, TestResult, TestCreate, QuestionCreate, QuestionChange, \
    QuestionDelete

urlpatterns = [
    path('', TestView.as_view(), name='list'),
    path('create/', TestCreate.as_view(), name='test_create'),
    path('change/<int:pk>/', TestChange.as_view(), name='test_change'),
    path('delete/<int:pk>/', TestDelete.as_view(), name='test_delete'),
    path('result/<int:pk>/', TestResult.as_view(), name='test_result'),
    path('<int:pk>/question/create/', QuestionCreate.as_view(), name='question_create'),
    path('<int:test_pk>/question/<int:question_pk>/change/', QuestionChange.as_view(), name='question_change'),
    path('<int:test_pk>/question/<int:question_pk>/delete/', QuestionDelete.as_view(), name='question_delete')
]
