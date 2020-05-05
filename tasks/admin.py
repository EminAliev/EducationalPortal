from django.contrib import admin
from django import forms

from tasks.models import Question, Answer, Test, CounterAnswer, TestSubject


def all_fields_admin(cls, *exclude_fields):
    return [field.name for field in cls._meta.fields if field.name not in exclude_fields]


class AdminQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        if 'on' not in self.get_variants():
            msg = 'Выберите верный вариант'
            self.add_error(None, msg)

        return super().clean()

    def get_variants(self):
        for k, v in self.data.items():
            if 'is_right' in k:
                yield v


class AdminQuestion(admin.ModelAdmin):
    """Админка вопросов"""

    class PossibleAnswerInline(admin.TabularInline):
        """
        Возможность добавления вариантов ответа
        сразу при создании вопроса
        """
        model = Answer

    form = AdminQuestionForm
    inlines = [
        PossibleAnswerInline,
    ]
    list_display = ("id", "question", "test")
    list_display_links = ("question",)


class AdminTest(admin.ModelAdmin):
    """Админка тестов"""

    class QuestionInline(admin.TabularInline):
        """
        Возможность добавления вопросов
        сразу при создании теста
        """
        model = Question

    list_display = all_fields_admin(Test)
    inlines = [
        QuestionInline,
    ]


class AdminPossibleAnswer(admin.ModelAdmin):
    """Админка вариантов ответа"""
    list_display = all_fields_admin(Answer)


class AnswersCounterAdmin(admin.ModelAdmin):
    """Ответы на тесты"""
    list_display = all_fields_admin(CounterAnswer)


admin.site.register(TestSubject)
admin.site.register(Test, AdminTest)
admin.site.register(Question, AdminQuestion)
admin.site.register(Answer, AdminPossibleAnswer)
admin.site.register(CounterAnswer, AnswersCounterAdmin)
