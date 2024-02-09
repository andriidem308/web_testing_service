from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
import boto3

from main.forms import (
    GroupCreateForm, GroupUpdateForm,
    LectureCreateForm, LectureUpdateForm, ProblemCreateForm, ProblemUpdateForm, ProblemTakeForm
)
from main.models import (
    Student, Teacher, Group, Lecture, Problem, Solution
)
from main.services import article_service
from main.services.code_solver import test_student_solution
from main.services.s3_helper import upload_file_to_s3
from main.services.users_service import get_teacher, get_student
from main.services import paginate_service
from web_testing_service import settings

from web_testing_service.settings import MEDIA_URL


PATH_TO_TEST_FILE = "tests.json"

def test(request):
    context = {'comments': ['Comment 1', 'Comment 2', 'Comment 3']}
    return render(request, 'index.html', context=context)


def index(request):
    return render(request, 'index.html')


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
        self.object_list = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)
        groups = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        context['groups'] = groups
        return self.render_to_response(context)


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


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/group_edit.html'
    success_url = reverse_lazy('groups')


class GroupDeleteView(DeleteView):
    model = Group
    success_url = reverse_lazy('groups')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


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
        self.object_list = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)
        lectures = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        context['lectures'] = lectures
        return self.render_to_response(context)


class LectureView(DetailView):
    model = Lecture
    context_object_name = 'lecture'
    template_name = 'lectures/lecture.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        teacher = get_teacher(self.request.user)
        student = get_student(self.request.user)

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
        form = LectureCreateForm(teacher, request.POST)
        if form.is_valid():
            form.save()
            return redirect('lectures')
        else:
            context = {'form': form, 'user': user}
            return render(request, self.template_name, context)


class LectureUpdateView(UpdateView):
    model = Lecture
    form_class = LectureUpdateForm
    template_name = 'lectures/lecture_edit.html'
    success_url = reverse_lazy('lectures')


class LectureDeleteView(DeleteView):
    model = Lecture
    success_url = reverse_lazy('lectures')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


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
        self.object_list = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)
        problems = paginate_service.create_paginator(request, self.object_list, limit=self.paginate_by)
        context['problems'] = problems
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        problems_list = context['object_list']
        for p in problems_list:
            p.date_created = p.date_created.strftime('%d/%m/%Y, %H:%M')
            p.deadline = p.deadline.strftime('%d/%m/%Y, %H:%M')
        return context


class ProblemView(DetailView):
    model = Problem
    context_object_name = 'problem'
    template_name = 'problems/problem.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        teacher = get_teacher(self.request.user)
        student = get_student(self.request.user)
        solution = article_service.solution_find(self.object, student) if student else None

        context = self.get_context_data(object=self.object)

        comment_form, comments = article_service.comment_method(self.object, self.request)

        test_filename = str(self.object.test_file).split('/')[-1]

        context.update({
            'date_created': self.object.date_created,
            'deadline': self.object.deadline,
            'comment_form': comment_form,
            'comments': comments,
            'teacher': teacher,
            'student': student,
            'solution': solution,
            'test_filename': test_filename,
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


class ProblemCreateView(CreateView):
    model = Problem
    form_class = ProblemCreateForm
    template_name = 'problems/problem_add.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = ProblemCreateForm(teacher=teacher)
        context = {'form': form, 'teacher': teacher}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        form = ProblemCreateForm(teacher, request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            instance = form.save(commit=False)
            instance.teacher = teacher

            if settings.workflow == 's3':
                instance.save()

                test_file = request.FILES.get('test_file')
                if test_file:
                    upload_file_to_s3(instance, test_file)

            elif settings.workflow == 'local':
                form.save()

            return redirect('problems')

        else:
            context = {'form': form, 'user': user}
            return render(request, self.template_name, context)


class ProblemUpdateView(UpdateView):
    model = Problem
    form_class = ProblemUpdateForm
    template_name = 'problems/problem_edit.html'
    success_url = reverse_lazy('problems')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        _, comments = article_service.comment_method(self.object, self.request)

        teacher = get_teacher(self.request.user)
        student = get_student(self.request.user)

        context = self.get_context_data(object=self.object)

        context.update({
            'date_created': self.object.date_created,
            'deadline': self.object.deadline,
            'comments': comments,
            'teacher': teacher,
            'student': student,
            'MEDIA_URL': MEDIA_URL,
        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        _, comments = article_service.comment_method(self.object, self.request)

        user = self.request.user
        teacher = get_teacher(user)
        form = self.get_form()

        if form.is_valid():
            form.save()
            return redirect('problem', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            context.update({
                'user': user,
                'form': form,
                'date_created': self.object.date_created,
                'deadline': self.object.deadline,
                'comments': comments,
                'teacher': teacher,
                # 'solution': solution,
                # 'test_filename': test_filename,
                'MEDIA_URL': MEDIA_URL,
                'errors': form.errors,
            })
            return render(request, self.template_name, context)


class ProblemDeleteView(DeleteView):
    model = Problem
    success_url = reverse_lazy('problems')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


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
            if settings.workflow == 's3':
                s3_path = problem.test_file.name
                if read_file_from_s3(s3_path, PATH_TO_TEST_FILE):
                    test_file = PATH_TO_TEST_FILE

            elif settings.workflow == 'local':
                test_file = problem.test_file
            solution_code = solution.solution_code
            max_execution_time = problem.max_execution_time

            test_score_percentage = test_student_solution(code=solution_code,
                                                          exec_time=max_execution_time,
                                                          test_filename=test_file)

            score = round(test_score_percentage * problem.max_points, 1)
            # if settings.workflow == 's3':

            print(score)

            if timezone.now() > problem.deadline:
                score = round(score / 2, 1)

            previous_solutions = Solution.objects.filter(student=student).filter(problem=problem)
            if previous_solutions:
                if score > previous_solutions[0].score:
                    previous_solutions.delete()
                    solution.score = score
                    solution.save()
            else:
                solution.score = score
                solution.save()

            return redirect('problem', pk=problem_id)
        else:
            context = {'form': form, 'user': user, 'student': student, 'problem': problem}
            return render(request, self.template_name, context)
