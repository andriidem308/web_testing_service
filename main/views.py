from django.shortcuts import render

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView


from main.models import *
from accounts.models import *
from main.forms import (
    GroupCreateForm, GroupUpdateForm,
    LectureCreateForm, LectureUpdateForm,
)

# def index(request):
#     return render(request, 'index.html')


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


def lectures(request):
    return render(request, 'lectures/lectures.html')


def lecture_add(request):
    return render(request, 'lectures/lecture_add.html')


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


def lecture(request, pk):
    return render(request, 'lectures/lecture.html')


def lecture_edit(request, pk):
    return render(request, 'lectures/lecture_edit.html')


def groups(request):
    return render(request, 'groups/groups.html')


def group_add(request):
    return render(request, 'groups/group_add.html')


def group(request, pk):
    return render(request, 'groups/group.html')
