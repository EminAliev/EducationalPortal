from django.urls import path

from tasks.views import TeacherTestView, TeacherTestChange, TeacherTestDelete, TeacherTestResult, TeacherTestCreate, \
    QuestionCreate, \
    QuestionDelete, question_change, StudentTestView, StudentCompleteTest, pass_test

urlpatterns = [
    path('', TeacherTestView.as_view(), name='list'),
    path('create/', TeacherTestCreate.as_view(), name='test_create'),
    path('change/<int:pk>/', TeacherTestChange.as_view(), name='test_change'),
    path('delete/<int:pk>/', TeacherTestDelete.as_view(), name='test_delete'),
    path('result/<int:pk>/', TeacherTestResult.as_view(), name='test_result'),
    path('<int:pk>/question/create/', QuestionCreate.as_view(), name='question_create'),
    path('<int:test_pk>/question/<int:question_pk>/change/', question_change, name='question_change'),
    path('<int:test_pk>/question/<int:question_pk>/delete/', QuestionDelete.as_view(), name='question_delete'),
    path('pass/', StudentTestView.as_view(), name='test_list'),
    path('pass/task', StudentCompleteTest.as_view(), name='complete_test'),
    path('<int:pk>/pass', pass_test, name='pass_test'),
]
