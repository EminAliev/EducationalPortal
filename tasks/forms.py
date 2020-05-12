from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from tasks.models import Question, Answer, StudentAnswerTest
from django import forms


class QuestionForm(forms.ModelForm):
    """Форма вопросов"""

    class Meta:
        model = Question
        fields = ('question_text',)


class TrueAnswerForm(forms.BaseInlineFormSet):
    """Форма правильных ответов """

    def clean(self):
        super().clean()
        correct = False
        for f in self.forms:
            if not f.cleaned_data.get('DELETE', False):
                if f.cleaned_data.get('correct_answer', False):
                    correct = True
                    break
        if not correct:
            raise ValidationError('У вас нет правильных ответов, добавить правильный ответ.', code='no_correct_answer')


# Получаем формы, когда объекты ответов, будут связаны с объектами вопросов
InlineAnswerFormSet = inlineformset_factory(Question, Answer, formset=TrueAnswerForm,
                                            fields=('answer', 'correct_answer'),
                                            min_num=2, validate_min=True, max_num=10, validate_max=True
                                            )
