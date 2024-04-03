from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.decorators import student_required, teacher_required
from core.settings import MEDIA_URL
from main.forms import GroupCreateForm, GroupUpdateForm, LectureCreateForm, LectureUpdateForm, TestCreateForm, \
    TestUpdateForm, QuestionCreateForm, ProblemCreateForm, ProblemUpdateForm, ProblemTakeForm, CheckSolutionForm, \
    QuestionTakeForm
from main.models import Teacher, Student, Group, Problem, Solution, Lecture, Notification, Test
from main.services import article_service, code_solver, notification_service, paginate_service, users_service


def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')


@method_decorator([login_required], name='dispatch')
class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'groups/groups.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('name')
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user

        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, user, show_all)

        context = super().get_context_data(*args, **kwargs)
        groups = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        teacher = users_service.get_teacher(request.user)
        context['groups'] = groups
        context['teacher'] = teacher
        return self.render_to_response(context)


@method_decorator([login_required], name='dispatch')
class GroupView(DetailView):
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        students = Student.objects.filter(group=self.object)
        students = paginate_service.create_paginator(request, students, limit=self.paginate_by)
        context = self.get_context_data(object=self.object, students=students)
        return self.render_to_response(context)


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupCreateView(CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'groups/group_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        teacher = Teacher.objects.get(user=self.request.user)
        kwargs['teacher'] = teacher
        return kwargs

    def get(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = GroupCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        teacher = Teacher.objects.get(user=user)
        form = GroupCreateForm(teacher, request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/group_edit.html'
    success_url = reverse_lazy('groups')


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    success_url = reverse_lazy('groups')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class LectureListView(ListView):
    model = Lecture
    context_object_name = 'lectures'
    template_name = 'lectures/lectures.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_updated')
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user

        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, user, show_all)

        context = super().get_context_data(*args, **kwargs)
        lectures = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        teacher = users_service.get_teacher(request.user)
        context['lectures'] = lectures
        context['teacher'] = teacher
        return self.render_to_response(context)


@method_decorator([login_required], name='dispatch')
class LectureView(DetailView):
    model = Lecture
    context_object_name = 'lecture'
    template_name = 'lectures/lecture.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        teacher = users_service.get_teacher(self.request.user)
        student = users_service.get_student(self.request.user)

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
    model = Lecture
    form_class = LectureCreateForm
    template_name = 'lectures/lecture_add.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = LectureCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = LectureCreateForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save()
            notification_service.mail_lecture_added_notify(lecture)
            notification_service.create_new_lecture_notification(lecture)
            return redirect('lectures')
        else:
            print(form.errors)

            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureUpdateView(UpdateView):
    model = Lecture
    form_class = LectureUpdateForm
    template_name = 'lectures/lecture_edit.html'
    success_url = reverse_lazy('lectures')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'form': LectureUpdateForm(instance=self.object),
            'date_created': self.object.date_created,
            'teacher': users_service.get_teacher(self.request.user),
            'student': users_service.get_student(self.request.user),
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
                'user': self.request.user,
                'form': form,
                'teacher': users_service.get_teacher(self.request.user),
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureDeleteView(DeleteView):
    model = Lecture
    success_url = reverse_lazy('lectures')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator([login_required], name='dispatch')
class TestListView(ListView):
    model = Test
    context_object_name = 'tests'
    template_name = 'tests/tests.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_updated')
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user

        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, user, show_all)

        context = super().get_context_data(*args, **kwargs)
        tests = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        teacher = users_service.get_teacher(request.user)
        context['tests'] = tests
        context['teacher'] = teacher
        return self.render_to_response(context)


@method_decorator([login_required], name='dispatch')
class TestView(DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/test.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        teacher = users_service.get_teacher(self.request.user)
        student = users_service.get_student(self.request.user)
        #student_answer = article_service.student_answer_find(self.object, student) if student else None
        context.update({
            'date_created': self.object.date_created,
            'teacher': teacher,
            'student': student,
            #'student_answer': student_answer,
        })

        return self.render_to_response(context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestCreateView(CreateView):
    model = Test
    form_class = TestCreateForm
    template_name = 'tests/test_add.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = TestCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = TestCreateForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            test = form.save()
            notification_service.mail_lecture_added_notify(test)
            notification_service.create_new_lecture_notification(test)
            return redirect('questions', pk=test.pk)
        else:
            print(form.errors)
            context = {'form': form}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestUpdateView(UpdateView):
    model = Test
    form_class = TestUpdateForm
    template_name = 'tests/test_edit.html'
    success_url = reverse_lazy('tests')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'form': TestUpdateForm(instance=self.object),
            'date_created': self.object.date_created,
            'teacher': users_service.get_teacher(self.request.user),
            'student': users_service.get_student(self.request.user),
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
                'user': self.request.user,
                'form': form,
                'teacher': users_service.get_teacher(self.request.user),
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestDeleteView(DeleteView):
    model = Test
    success_url = reverse_lazy('tests')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def questions(request, **kwargs):
    test = Test.objects.get(pk=kwargs.get('pk'))
    context = {
        'test': test,
        'form': QuestionCreateForm(test),
    }
    return render(request, 'tests/add_questions.html', context=context)


def question_add(request, **kwargs):
    test = Test.objects.get(pk=kwargs.get('pk'))

    if request.method == 'POST':
        form = QuestionCreateForm(test, request.POST or None)

        print(form.errors)

        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            context = {'question': question, 'test': test}
            return render(request, 'tests/question_add.html', context=context)

    context = {'form': QuestionCreateForm(test), 'test': test}
    return render(request, 'tests/question_add.html', context=context)


@method_decorator([login_required, student_required], name='dispatch')
class TestTakeView(CreateView):
    model = Test
    template_name = 'tests/test_take.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        student = Student.objects.get(user=user)
        test = Test.objects.get(id=kwargs.get('pk'))
        context = {'student': student, 'test': test}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        test_id = kwargs.get('pk')
        test = Problem.objects.get(id=test_id)

        user = self.request.user
        student = Student.objects.get(user=user)


def question_show(request, **kwargs):
    test = Test.objects.get(pk=kwargs.get('pk'))
    user = request.user
    student = Student.objects.get(user=user)

    if request.method == 'POST':
        form = QuestionTakeForm(test, student)

        print(form.errors)

        if form.is_valid():
            student_answers = form.save(commit=False)
            student_answers.save()
            context = {'student_answers': student_answers, 'test': test}
            return render(request, 'tests/question_show.html', context=context)

    context = {'form': QuestionTakeForm(test, student), 'test': test}
    return render(request, 'tests/question_show.html', context=context)


@method_decorator([login_required], name='dispatch')
class ProblemListView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'problems/problems.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_updated')
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user

        show_all = request.GET.get('show_all')

        queryset = self.get_queryset()
        self.object_list = users_service.filter_common_queryset(queryset, user, show_all)
        context = super().get_context_data(*args, **kwargs)

        user = request.user

        teacher = users_service.get_teacher(user)
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
    model = Problem
    context_object_name = 'problem'
    template_name = 'problems/problem.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        teacher = users_service.get_teacher(self.request.user)
        solutions = article_service.solutions_by_problem(self.object).order_by('checked')

        student = users_service.get_student(self.request.user)
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
    model = Problem
    form_class = ProblemCreateForm
    template_name = 'problems/problem_add.html'

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=self.request.user)
        context = {'form': ProblemCreateForm(teacher)}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=self.request.user)
        form = ProblemCreateForm(teacher, request.POST, request.FILES)

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
    model = Problem
    form_class = ProblemUpdateForm
    template_name = 'problems/problem_edit.html'
    success_url = reverse_lazy('problems')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({
            'form': ProblemUpdateForm(instance=self.object),
            'date_created': self.object.date_created,
            'deadline': self.object.deadline,
            'teacher': users_service.get_teacher(self.request.user),
            'student': users_service.get_student(self.request.user),
        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = ProblemUpdateForm(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            form.save()
            return redirect('problem', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            context.update({
                'user': self.request.user,
                'form': form,
                'teacher': users_service.get_teacher(self.request.user),
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemDeleteView(DeleteView):
    model = Problem
    success_url = reverse_lazy('problems')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator([login_required, student_required], name='dispatch')
class ProblemTakeView(CreateView):
    model = Solution
    form_class = ProblemTakeForm
    template_name = 'problems/problem_take.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        student = Student.objects.get(user=user)
        problem = Problem.objects.get(id=kwargs.get('pk'))

        form = ProblemTakeForm(problem=problem, student=student)
        context = {'form': form, 'student': student, 'problem': problem}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        problem_id = kwargs.get('pk')
        problem = Problem.objects.get(id=problem_id)

        user = self.request.user
        student = Student.objects.get(user=user)

        form = ProblemTakeForm(problem, student, request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.problem = problem
            solution.student = student

            code_solver.problem_take(solution)

            return redirect('problem', pk=problem_id)
        else:
            context = {'form': form, 'user': user, 'student': student, 'problem': problem}
            return render(request, self.template_name, context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemSolutionListView(ListView):
    model = Solution
    context_object_name = 'solutions'
    template_name = 'problems/problem_solutions.html'
    paginate_by = 12

    def get_queryset(self):
        problem_id = self.kwargs.get('pk')
        problem = Problem.objects.get(id=problem_id)
        queryset = article_service.solutions_by_problem(problem)
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user

        self.object_list = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)

        teacher = users_service.get_teacher(user)
        problem = Problem.objects.get(id=self.kwargs.get('pk'))
        solutions = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)

        context.update({
            'problem': problem,
            'solutions': solutions,
            'teacher': teacher,
        })

        return self.render_to_response(context)


@method_decorator([login_required], name='dispatch')
class ProblemSolutionView(DetailView):
    model = Solution
    context_object_name = 'solution'
    template_name = 'problems/solution.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        solution_code = self.object.solution_code

        context = super().get_context_data(**kwargs)
        context['solution_code'] = solution_code

        teacher = users_service.get_teacher(request.user)
        if teacher and not self.object.checked:
            form = CheckSolutionForm(instance=self.object)
            form.fields['formatted_score'].initial = self.object.points
            context['form'] = form
            context['teacher'] = teacher

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = CheckSolutionForm(request.POST, instance=self.object)

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


def view_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    object_type = notification.object_type
    object_id = notification.object_id
    notification.is_seen = True
    notification.save()
    return redirect(object_type, pk=object_id)
