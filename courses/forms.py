from django import forms
from django.forms import Textarea
from django.forms.models import inlineformset_factory

from courses.models import Course, Module, MessagesTask, Comment

"""Получаем формы, когда объекты модулей, будут связаны с объектами курсов"""
CourseModuleFormSet = inlineformset_factory(Course, Module, fields=['name', 'definition'], extra=2, can_delete=True)


class AnswerForm(forms.ModelForm):
    """Форма ответа на задание"""

    class Meta:
        model = MessagesTask
        fields = ("answer",)


class CommentForm(forms.ModelForm):
    """Форма комментария(отзыва) к курсу"""

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows': 5})
