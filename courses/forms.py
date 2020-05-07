from django import forms
from django.forms.models import inlineformset_factory

from courses.models import Course, Module, MessagesTask

"""Получаем формы, когда объекты модулей, будут связаны с объектами курсов"""
CourseModuleFormSet = inlineformset_factory(Course, Module, fields=['name', 'definition'], extra=2, can_delete=True)


class AnswerForm(forms.ModelForm):
    """Форма ответа на задание"""

    class Meta:
        model = MessagesTask
        fields = ("answer",)
