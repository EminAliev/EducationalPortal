from django.contrib import admin

from tasks.models import Test, Question, Answer, CompleteTest, StudentAnswerTest
from users.models import Student


class QuestionInline(admin.StackedInline):
    model = Question


class AnswerInline(admin.StackedInline):
    model = Answer


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Админка тестов"""
    list_display = ['author', 'name', 'course']
    search_fields = ['name', 'course']
    list_filter = ['course']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка вопросов"""
    list_display = ['test', 'question_text']
    search_fields = ['test']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Админка ответов"""
    list_display = ['question', 'answer', 'correct_answer']
    search_fields = ['answer']


@admin.register(CompleteTest)
class CompleteTestAdmin(admin.ModelAdmin):
    """Админка выполненных тестов"""
    list_display = ['student', 'test', 'result', 'date_created']
    search_fields = ['student', 'test']
    list_filter = ['date_created', 'test']


@admin.register(StudentAnswerTest)
class StudentAnswerTestAdmin(admin.ModelAdmin):
    """Админка ответа студента"""
    list_display = ['student', 'answer_text']
