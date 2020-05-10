from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Avg
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import View, TemplateResponseMixin
from functools import wraps

from tasks.forms import QuestionForm, InlineAnswerFormSet, PassTestForm
from tasks.models import Test, Question, CompleteTest
from users.views import TeacherRequiredMixin, StudentRequiredMixin, teacher_required, student_required


class TeacherTestView(TeacherRequiredMixin, LoginRequiredMixin, ListView):
    """Список тестов"""
    model = Test
    ordering = ('name',)
    context_object_name = 'test'
    template_name = 'tasks/teacher/test/test_list.html'

    def get_queryset(self):
        qs = self.request.user.test.select_related('course').annotate(
            questions_count=Count('questions', distinct=True)).annotate(
            taken_count=Count('complete_test', distinct=True))
        return qs


class TeacherTestCreate(TeacherRequiredMixin, LoginRequiredMixin, CreateView):
    """Создание тестов"""
    model = Test
    fields = ('name', 'course',)
    template_name = 'tasks/teacher/test/test_create.html'

    def form_valid(self, form):
        test = form.save(commit=False)
        test.author = self.request.user
        test.save()
        return redirect('test_change', test.pk)


class TeacherTestChange(TeacherRequiredMixin, LoginRequiredMixin, UpdateView):
    """Изменение теста"""
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


class TeacherTestDelete(TeacherRequiredMixin, LoginRequiredMixin, DeleteView):
    """Удаление теста"""
    model = Test
    context_object_name = 'test'
    template_name = 'tasks/teacher/test/test_delete.html'
    success_url = reverse_lazy('list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.test.all()


class TeacherTestResult(TeacherRequiredMixin, LoginRequiredMixin, DetailView):
    """Результаты тестов"""
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
    """Создание нового вопроса"""
    model = Question
    template_name = 'tasks/teacher/question/question_create.html'

    def get(self, request, pk, *args, **kwargs):
        form = QuestionForm()
        return self.render_to_response({'form': form})

    def post(self, request, pk):
        test = get_object_or_404(Test, pk=pk, author=request.user)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect('question_change', test.pk, question.pk)
        else:
            form = QuestionForm()
        return self.render_to_response({'test': test, 'form': form})


@login_required
@teacher_required
def question_change(request, test_pk, question_pk):
    """Изменение вопроса и добавление к вопросу ответы"""
    test = get_object_or_404(Test, pk=test_pk, author=request.user)
    question = get_object_or_404(Question, pk=question_pk, test=test)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        answer_formset = InlineAnswerFormSet(request.POST, instance=question)
        if question_form.is_valid() and answer_formset.is_valid():
            with transaction.atomic():
                question_form.save()
                answer_formset.save()
            return redirect('test_change', test.pk)
    else:
        question_form = QuestionForm(instance=question)
        answer_formset = InlineAnswerFormSet(instance=question)

    return render(request, 'tasks/teacher/question/question_change.html', {
        'test': test,
        'question': question,
        'question_form': question_form,
        'answer_formset': answer_formset
    })


class QuestionDelete(TeacherRequiredMixin, LoginRequiredMixin, DeleteView):
    """Удаление вопроса"""
    model = Question
    context_object_name = 'question'
    template_name = 'tasks/teacher/question/question_delete.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['test'] = question.test
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(test__author=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('test_change', kwargs={'pk': question.test_id})


class StudentTestView(StudentRequiredMixin, LoginRequiredMixin, ListView):
    model = Test
    ordering = ('name',)
    context_object_name = 'test'
    template_name = 'tasks/student/list.html'

    def get_queryset(self):
        qs = Test.objects.all()
        return qs


class StudentCompleteTest(ListView):
    model = CompleteTest
    context_object_name = 'complete_test'
    template_name = 'tasks/student/all_complete_test.html'

    def get_queryset(self):
        qs = self.request.user.student.complete_test.select_related('test', 'test__course').order_by('test__name')
        return qs


@login_required
@student_required
def pass_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    student = request.user.student

    if student.test.filter(pk=pk).exists():
        return render(request, 'tasks/student/complete_test.html')

    all_questions = test.questions.count()
    not_completed_questions = student.get_not_completed_questions(test)
    all_not_completed_questions = not_completed_questions.count()
    print(not_completed_questions, all_not_completed_questions)
    result = 100 - round(((all_not_completed_questions - 1) / all_questions) * 100)
    question = not_completed_questions.first()

    if request.method == 'POST':
        pass_form = PassTestForm(question=question, data=request.POST)
        if pass_form.is_valid():
            with transaction.atomic():
                student_answer = pass_form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_not_completed_questions(test).exists():
                    return redirect('pass_test', pk)
                else:
                    correct_answers = student.tests_answers.filter(answer__question__test=test,
                                                                   answer__correct_answer=True).count()
                    result = round((correct_answers / all_questions) * 100.0, 2)
                    CompleteTest.objects.create(student=student, test=test, result=result)
                    return redirect('test_list')
    else:
        pass_form = PassTestForm(question=question)
    return render(request, 'tasks/student/complete_test.html', {
        'test': test,
        'question': question,
        'pass_form': pass_form,
        'result': result
    })
