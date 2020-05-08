from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count, Avg
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import View, TemplateResponseMixin

from tasks.forms import QuestionForm, InlineAnswerFormSet
from tasks.models import Test, Question
from users.views import TeacherRequiredMixin


class TestView(TeacherRequiredMixin, LoginRequiredMixin, ListView):
    model = Test
    ordering = ('name',)
    context_object_name = 'test'
    template_name = 'tasks/teacher/test/test_list.html'

    def get_queryset(self):
        qs = self.request.user.test.select_related('course').annotate(
            questions_count=Count('questions', distinct=True)).annotate(
            taken_count=Count('complete_test', distinct=True))
        return qs


class TestCreate(TeacherRequiredMixin, LoginRequiredMixin, CreateView):
    model = Test
    fields = ('name', 'course',)
    template_name = 'tasks/teacher/test/test_create.html'

    def form_valid(self, form):
        test = form.save(commit=False)
        test.author = self.request.user
        test.save()
        return redirect('test_change', test.pk)


class TestChange(TeacherRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Test
    fields = ('name', 'course',)
    context_object_name = 'test'
    template_name = 'tasks/teacher/test/test_change.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.test.all()

    def get_success_url(self):
        return reverse('test_change', kwargs={'pk': self.object.pk})


class TestDelete(TeacherRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Test
    context_object_name = 'test'
    template_name = 'tasks/teacher/test/test_delete.html'
    success_url = reverse_lazy('list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.test.all()


class TestResult(TeacherRequiredMixin, LoginRequiredMixin, DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'tasks/teacher/test/test_result.html'

    def get_context_data(self, **kwargs):
        test = self.get_object()
        complete_test = test.complete_test.select_related('student__user').order_by('-date_created')
        all_complete_tests = complete_test.count()
        result = test.complete_test.aggregate(average_score=Avg('result'))
        extra_context = {'complete_test': complete_test, 'all_complete_tests': all_complete_tests, 'result': result}
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.test.all()


class QuestionCreate(TeacherRequiredMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    model = Question
    template_name = ''

    def post(self, request, pk):
        test = get_object_or_404(Test, pk=pk, author=request.user)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect('change_question', test.pk, question.pk)
        else:
            form = QuestionForm()
        return self.render_to_response({'test': test, 'form': form})


class QuestionChange(TeacherRequiredMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    model = Question
    template_name = ""

    def post(self, request, test_pk, question_pk):
        test = get_object_or_404(Test, pk=test_pk, author=request.user)
        question = get_object_or_404(Question, pk=question_pk, test=test)
        form = QuestionForm(request.POST, instance=question)
        answer_formset = InlineAnswerFormSet(request.POST, instance=question)
        if form.is_valid() and answer_formset.is_valid():
            with transaction.atomic():
                form.save()
                answer_formset.save()
            return redirect('test_change', test.pk)
        else:
            form = QuestionForm(instance=question)
            answer_formset = InlineAnswerFormSet(instance=question)
        return self.render_to_response({'test': test,
                                        'question': question,
                                        'form': form,
                                        'answer_formset': answer_formset})


class QuestionDelete(TeacherRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = ''
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['test'] = question.test
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__author=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('test_change', kwargs={'pk': question.test_id})
