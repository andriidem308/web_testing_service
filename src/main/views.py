from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.decorators import student_required, teacher_required
from core.settings import MEDIA_URL
from main import forms, models
from main.services import article_service, code_solver, notification_service, paginate_service, users_service
from main.services.users_service import get_teacher, get_students_by_group, get_student


def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupListView(ListView):
    model = models.Group
    context_object_name = 'groups'
    template_name = 'groups/groups.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('name')
        return queryset

    def get(self, request, *args, **kwargs):
        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, request, show_all)

        context = super().get_context_data(*args, **kwargs)
        groups = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        teacher = users_service.get_teacher(request)
        context['groups'] = groups
        context['teacher'] = teacher
        return self.render_to_response(context)


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupView(DetailView):
    model = models.Group
    context_object_name = 'group'
    template_name = 'groups/group.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        students = get_students_by_group(self.object)
        students = paginate_service.create_paginator(request, students, limit=self.paginate_by)
        context = self.get_context_data(object=self.object, students=students)
        return self.render_to_response(context)


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupCreateView(CreateView):
    model = models.Group
    form_class = forms.GroupCreateForm
    template_name = 'groups/group_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        teacher = get_teacher(self.request)
        kwargs['teacher'] = teacher
        return kwargs

    def get(self, request, *args, **kwargs):
        teacher = get_teacher(request)
        form = forms.GroupCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = get_teacher(request)
        form = forms.GroupCreateForm(teacher, request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupUpdateView(UpdateView):
    model = models.Group
    form_class = forms.GroupUpdateForm
    template_name = 'groups/group_edit.html'
    success_url = reverse_lazy('groups')


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupDeleteView(DeleteView):
    model = models.Group
    success_url = reverse_lazy('groups')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class LectureListView(ListView):
    model = models.Lecture
    context_object_name = 'lectures'
    template_name = 'lectures/lectures.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_updated')
        return queryset

    def get(self, request, *args, **kwargs):
        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, request, show_all)

        context = super().get_context_data(*args, **kwargs)
        lectures = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        teacher = users_service.get_teacher(request)
        context['lectures'] = lectures
        context['teacher'] = teacher
        return self.render_to_response(context)


@method_decorator([login_required], name='dispatch')
class LectureView(DetailView):
    model = models.Lecture
    context_object_name = 'lecture'
    template_name = 'lectures/lecture.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        teacher = users_service.get_teacher(self.request)
        student = users_service.get_student(self.request)

        comment_form, comments = article_service.comment_method(self.object, self.request)

        context.update({
            'date_created': self.object.date_created,
            'comment_form': comment_form,
            'comments': comments,
            'teacher': teacher,
            'student': student,
        })

        context['comment_form'] = comment_form
        context['comments'] = comments

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        comment_form, comments = article_service.comment_method(self.object, self.request)
        context = self.get_context_data(object=self.object)

        context['comment_form'] = comment_form
        context['comments'] = comments

        return redirect('lecture', pk=self.object.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureCreateView(CreateView):
    model = models.Lecture
    form_class = forms.LectureCreateForm
    template_name = 'lectures/lecture_add.html'

    def get(self, request, *args, **kwargs):
        teacher = get_teacher(request)
        form = forms.LectureCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = get_teacher(request)
        form = forms.LectureCreateForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save()
            notification_service.mail_lecture_added_notify(lecture)
            notification_service.create_new_lecture_notification(lecture)
            return redirect('lectures')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureUpdateView(UpdateView):
    model = models.Lecture
    form_class = forms.LectureUpdateForm
    template_name = 'lectures/lecture_edit.html'
    success_url = reverse_lazy('lectures')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'form': forms.LectureUpdateForm(instance=self.object),
            'date_created': self.object.date_created,
            'teacher': users_service.get_teacher(self.request),
            'student': users_service.get_student(self.request),
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():
            form.save()
            return redirect('lecture', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            context.update({
                'form': form,
                'teacher': users_service.get_teacher(self.request),
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureDeleteView(DeleteView):
    model = models.Lecture
    success_url = reverse_lazy('lectures')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class TestListView(ListView):
    model = models.Test
    context_object_name = 'tests'
    template_name = 'tests/tests.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_updated')
        return queryset

    def get(self, request, *args, **kwargs):
        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, request, show_all)

        context = super().get_context_data(*args, **kwargs)
        tests = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        teacher = users_service.get_teacher(request)
        context['tests'] = tests
        context['teacher'] = teacher
        return self.render_to_response(context)


@method_decorator([login_required], name='dispatch')
class TestView(DetailView):
    model = models.Test
    context_object_name = 'test'
    template_name = 'tests/test.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        teacher = users_service.get_teacher(self.request)
        student = users_service.get_student(self.request)
        # student_answer = article_service.student_answer_find(self.object, student) if student else None
        test_solution = models.TestSolution.objects.filter(student=student, test=self.object)
        test_solution = test_solution[0] if test_solution else None

        context.update({
            'date_created': self.object.date_created,
            'teacher': teacher,
            'student': student,
            'test_solution': test_solution
            # 'student_answer': student_answer,
        })

        return self.render_to_response(context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestCreateView(CreateView):
    model = models.Test
    form_class = forms.TestCreateForm
    template_name = 'tests/test_add.html'

    def get(self, request, *args, **kwargs):
        teacher = get_teacher(self.request)
        form = forms.TestCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = get_teacher(self.request)
        form = forms.TestCreateForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            test = form.save()
            notification_service.mail_test_added_notify(test)
            notification_service.create_new_test_notification(test)
            return redirect('questions', pk=test.pk)
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestUpdateView(UpdateView):
    model = models.Test
    form_class = forms.TestUpdateForm
    template_name = 'tests/test_edit.html'
    success_url = reverse_lazy('tests')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'form': forms.TestUpdateForm(instance=self.object),
            'date_created': self.object.date_created,
            'teacher': users_service.get_teacher(self.request),
            'student': users_service.get_student(self.request),
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():
            form.save()
            return redirect('test', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            context.update({
                'form': form,
                'teacher': users_service.get_teacher(self.request),
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestDeleteView(DeleteView):
    model = models.Test
    success_url = reverse_lazy('tests')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@teacher_required
@login_required
def questions(request, **kwargs):
    test = models.Test.objects.get(pk=kwargs.get('pk'))
    context = {
        'test': test,
        'form': forms.QuestionCreateForm(test),
    }
    return render(request, 'tests/add_questions.html', context=context)


@teacher_required
@login_required
def question_add(request, **kwargs):
    test = models.Test.objects.get(pk=kwargs.get('pk'))

    if request.method == 'POST':
        form = forms.QuestionCreateForm(test, request.POST or None)

        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            context = {'question': question, 'test': test}
            return render(request, 'tests/question_add.html', context=context)

    context = {'form': forms.QuestionCreateForm(test), 'test': test}
    return render(request, 'tests/question_add.html', context=context)


@student_required
@login_required
def test_take(request, **kwargs):
    test = models.Test.objects.get(pk=kwargs.get('pk'))

    questions = models.Question.objects.filter(test=test).order_by('?')
    student = get_student(request)

    found_test_solution = models.TestSolution.objects.filter(test=test, student=student)
    if found_test_solution:
        raise PermissionDenied

    test_solution = models.TestSolution(test=test, student=student, score=0)
    student_answers_forms = [forms.QuestionTakeForm(test_solution, question) for question in questions]

    if request.method == 'POST':
        correct_answers = 0
        total_answers = len(questions)

        answer_forms = []

        for question in questions:
            form = forms.QuestionTakeForm(test_solution, question, request.POST)

            if not form.is_valid():
                break

            if all([
                form.cleaned_data['answer_1'] == question.answer_1_correct,
                form.cleaned_data['answer_2'] == question.answer_2_correct,
                form.cleaned_data['answer_3'] == question.answer_3_correct,
                form.cleaned_data['answer_4'] == question.answer_4_correct,
            ]):
                correct_answers += 1

            answer_forms.append(form)

        else:
            test_solution.score = correct_answers / total_answers
            test_solution.save()

            for form in answer_forms:
                form.save()

            return redirect('test', pk=test.pk)

    context = {
        'test': test,
        'student': student,
        'questions': questions,
        'student_answers_forms': student_answers_forms,
    }
    return render(request, 'tests/test_take.html', context=context)


@method_decorator([login_required], name='dispatch')
class ProblemListView(ListView):
    model = models.Problem
    context_object_name = 'problems'
    template_name = 'problems/problems.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_updated')
        return queryset

    def get(self, request, *args, **kwargs):
        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, request, show_all)
        context = super().get_context_data(*args, **kwargs)

        teacher = users_service.get_teacher(request)
        problems = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)

        context.update({
            'problems': problems,
            'teacher': teacher,
        })

        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        problems_list = context['object_list']
        for p in problems_list:
            p.date_created = p.date_created.strftime('%d/%m/%Y, %H:%M')
            p.deadline = p.deadline.strftime('%d/%m/%Y, %H:%M')
        return context


@method_decorator([login_required], name='dispatch')
class ProblemView(DetailView):
    model = models.Problem
    context_object_name = 'problem'
    template_name = 'problems/problem.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        teacher = users_service.get_teacher(self.request)
        solutions = article_service.solutions_by_problem(self.object).order_by('checked')

        student = users_service.get_student(self.request)
        solution = article_service.solution_find(self.object, student) if student else None

        context = self.get_context_data(object=self.object)

        comment_form, comments = article_service.comment_method(self.object, self.request)

        context.update({
            'date_created': self.object.date_created,
            'deadline': self.object.deadline,
            'comment_form': comment_form,
            'comments': comments,
            'teacher': teacher,
            'student': student,
            'solution': solution,
            'solutions': solutions,
            'MEDIA_URL': MEDIA_URL,
        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        comment_form, comments = article_service.comment_method(self.object, self.request)
        context = self.get_context_data(problem=self.object)

        context.update({
            'date_created': self.object.date_created.strftime('%d/%m/%Y, %H:%M'),
            'deadline': self.object.deadline.strftime('%d/%m/%Y, %H:%M'),
            'comment_form': comment_form,
            'comments': comments,
            'MEDIA_URL': MEDIA_URL,
        })

        return redirect('problem', pk=self.object.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemCreateView(CreateView):
    model = models.Problem
    form_class = forms.ProblemCreateForm
    template_name = 'problems/problem_add.html'

    def get(self, request, *args, **kwargs):
        teacher = get_teacher(self.request)
        context = {'form': forms.ProblemCreateForm(teacher)}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = get_teacher(self.request)
        form = forms.ProblemCreateForm(teacher, request.POST, request.FILES)

        if form.is_valid():
            problem = form.save()
            notification_service.create_new_problem_notifications(problem)
            notification_service.mail_problem_added_notify(problem)
            return redirect('problems')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemUpdateView(UpdateView):
    model = models.Problem
    form_class = forms.ProblemUpdateForm
    template_name = 'problems/problem_edit.html'
    success_url = reverse_lazy('problems')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'form': forms.ProblemUpdateForm(instance=self.object),
            'date_created': self.object.date_created,
            'deadline': self.object.deadline,
            'teacher': users_service.get_teacher(self.request),
            'student': users_service.get_student(self.request),
        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = forms.ProblemUpdateForm(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            form.save()
            return redirect('problem', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            context.update({
                'form': form,
                'teacher': users_service.get_teacher(self.request),
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemDeleteView(DeleteView):
    model = models.Problem
    success_url = reverse_lazy('problems')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator([login_required, student_required], name='dispatch')
class ProblemTakeView(CreateView):
    model = models.Solution
    form_class = forms.ProblemTakeForm
    template_name = 'problems/problem_take.html'

    def get(self, request, *args, **kwargs):
        student = get_student(self.request)
        problem = models.Problem.objects.get(id=kwargs.get('pk'))

        form = forms.ProblemTakeForm(problem=problem, student=student)
        context = {'form': form, 'student': student, 'problem': problem}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        problem_id = kwargs.get('pk')
        problem = models.Problem.objects.get(id=problem_id)

        student = get_student(self.request)

        form = forms.ProblemTakeForm(problem, student, request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.problem = problem
            solution.student = student

            code_solver.problem_take(solution)

            return redirect('problem', pk=problem_id)
        else:
            context = {'form': form, 'student': student, 'problem': problem}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemSolutionListView(ListView):
    model = models.Solution
    context_object_name = 'solutions'
    template_name = 'problems/problem_solutions.html'
    paginate_by = 12

    def get_queryset(self):
        problem_id = self.kwargs.get('pk')
        problem = models.Problem.objects.get(id=problem_id)
        queryset = article_service.solutions_by_problem(problem)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)

        teacher = users_service.get_teacher(request)
        problem = models.Problem.objects.get(id=self.kwargs.get('pk'))
        solutions = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)

        context.update({
            'problem': problem,
            'solutions': solutions,
            'teacher': teacher,
        })

        return self.render_to_response(context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemSolutionView(DetailView):
    model = models.Solution
    context_object_name = 'solution'
    template_name = 'problems/solution.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        solution_code = self.object.solution_code

        context = super().get_context_data(**kwargs)
        context['solution_code'] = solution_code

        teacher = users_service.get_teacher(request)
        if teacher and not self.object.checked:
            form = forms.CheckSolutionForm(instance=self.object)
            form.fields['formatted_score'].initial = self.object.points
            context['form'] = form
            context['teacher'] = teacher

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = forms.CheckSolutionForm(request.POST, instance=self.object)

        if form.is_valid():
            solution = form.save(commit=False)
            max_points = self.object.problem.max_points

            formatted_score = form.cleaned_data.get('formatted_score')
            score = formatted_score / max_points
            solution.score = min(score, 1)

            solution.checked = True

            notification_service.create_solution_checked_notification(solution)
            solution.save()

            return redirect('solution', pk=self.object.pk)
        else:
            context = {'form': form, 'solution_code': self.object.solution_code}
            return self.render_to_response(context)


@login_required
def view_notification(request, pk):
    notification = models.Notification.objects.get(id=pk)
    object_type = notification.object_type
    object_id = notification.object_id
    notification.is_seen = True
    notification.save()
    return redirect(object_type, pk=object_id)
