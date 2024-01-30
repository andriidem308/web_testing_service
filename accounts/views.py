from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView

from accounts.models import User
from main.models import Teacher, Student
from main import forms, student_forms, teacher_forms


# Create your views here.

def profile(request):
    user: User = request.user
    if user.is_teacher:
        user_type = 'teacher'
        person = Teacher.objects.get(user=user)
    elif user.is_student:
        user_type = 'student'
        person = Student.objects.get(user=user)
    else:
        user_type = None
        person = None

    return render(request, 'profile.html',
                  context={'user': user, 'person': person, 'user_type': user_type})

def _login(request):
    return render(request, 'login.html')


class LoginView(BaseLoginView):
    model = User
    form_class = forms.AuthenticationForm
    template_name = 'login.html'


class SignUpTeacherView(CreateView):
    model = User
    form_class = teacher_forms.TeacherSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:problems')


class SignUpStudentView(CreateView):
    model = User
    form_class = student_forms.StudentSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:problem_list')


class SignUpView(CreateView):
    model = User
    form_class = forms.SignUpForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        form = forms.SignUpForm(user_type=user_type)
        context = {'form': form, 'user_type': user_type}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        form = forms.SignUpForm(request.POST, user_type=user_type)
        if form.is_valid():
            user = form.save(user_type)
            login(self.request, user)
            return redirect('profile')
        else:
            context = {'form': form, 'user_type': user_type}
            return render(request, self.template_name, context)


def signup(request):
    return render(request, 'signup.html')


def signupt(request):
    context = {'user_type': 'teacher'}
    return render(request, 'signup_form.html', context=context)

def signups(request):
    context = {'user_type': 'student'}
    return render(request, 'signup_form.html', context=context)


def signup_teacher(request):
    return render(request, 'signup_teacher.html')


def signup_student(request):
    return render(request, 'signup_student.html')
