import datetime

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from main.services.article_service import comment_method


from main.forms import (
    GroupCreateForm, GroupUpdateForm,
    LectureCreateForm, LectureUpdateForm, ProblemCreateForm,
)
from main.models import (
    Student, Teacher, Group, Lecture, Problem
)


def test(request):
    return render(request, 'test.html')

def index(request):
    return render(request, 'index.html')


def problems(request):
    return render(request, 'problems/problems.html')


def problem_add(request):
    return render(request, 'problems/problem_add.html')


def problem(request, pk):
    return render(request, 'problems/problem.html')


def problem_edit(request, pk):
    return render(request, 'problems/problem_edit.html')


def problem_take(request, pk):
    return render(request, 'problems/problem_take.html')


class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'groups/groups.html'


class GroupView(DetailView):
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group.html'


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


class LectureListView(ListView):
    model = Lecture
    context_object_name = 'lectures'
    template_name = 'lectures/lectures.html'


class LectureView(DetailView):
    model = Lecture
    context_object_name = 'lecture'
    template_name = 'lectures/lecture.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        comment_form, comments = comment_method(self.object, self.request)

        context['comment_form'] = comment_form
        context['comments'] = comments

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        comment_form, comments = comment_method(self.object, self.request)
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


# TODO: Problem views
class ProblemListView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'problems/problems.html'

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
        context = self.get_context_data(object=self.object)

        comment_form, comments = comment_method(self.object, self.request)

        context['date_created'] = self.object.date_created.strftime('%d/%m/%Y, %H:%M')
        context['deadline'] = self.object.deadline.strftime('%d/%m/%Y, %H:%M')
        context['comment_form'] = comment_form
        context['comments'] = comments

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        comment_form, comments = comment_method(self.object, self.request)
        context = self.get_context_data(object=self.object)
        context['date_created'] = self.object.date_created.strftime('%d/%m/%Y, %H:%M')
        context['deadline'] = self.object.deadline.strftime('%d/%m/%Y, %H:%M')
        context['comment_form'] = comment_form
        context['comments'] = comments

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
        form = ProblemCreateForm(teacher, request.POST)
        print(form.errors)
        if form.is_valid():
            print('a')
            form.save()
            return redirect('problems')
        else:
            print(form.data)
            context = {'form': form, 'user': user}
            return render(request, self.template_name, context)


class ProblemUpdateView(UpdateView):
    pass
    # model = Problem
    # form_class = ProblemUpdateForm
    # template_name = 'problems/problem_edit.html'
    # success_url = reverse_lazy('problems')
