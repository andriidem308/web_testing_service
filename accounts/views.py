from django.shortcuts import render
from django.views.generic import TemplateView

# from accounts.models import User, Student, Teacher


# Create your views here.

def login(request):
    return render(request, 'login.html')


# class LoginView(TemplateView):
#     pass
#
#
# class SignUpTeacherView(TemplateView):
#     model = User
#     form_class = TeacherSignUpForm
#     template_name = 'accounts/signup_form.html'
#
#
# class SignUpStudentView(TemplateView):
#     pass


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
