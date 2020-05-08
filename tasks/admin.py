"""from django.contrib import admin
from django import forms

from tasks.models import Question, Answer, Test


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

    class AnswerInline(admin.TabularInline):
        model = Answer

    form = AdminQuestionForm
    inlines = [
        AnswerInline,
    ]
    list_display = ("id", "question", "test")
    list_display_links = ("question",)


class AdminTest(admin.ModelAdmin):

    class QuestionInline(admin.TabularInline):
        model = Question

    list_display = all_fields_admin(Test)
    inlines = [
        QuestionInline,
    ]


class AdminAnswer(admin.ModelAdmin):
    list_display = all_fields_admin(Answer)




admin.site.register(Test, AdminTest)
admin.site.register(Question, AdminQuestion)
admin.site.register(Answer, AdminAnswer)"""
