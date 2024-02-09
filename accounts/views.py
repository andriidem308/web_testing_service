from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from accounts.forms import AuthenticationForm, SignUpForm
from accounts.models import User
from main.models import Student, Teacher


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


class LoginView(BaseLoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get('next') or ''
        form = AuthenticationForm()
        context = {'form': form, 'next_page': next_page}
        return render(request, self.template_name, context)


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        form = SignUpForm(user_type=user_type)
        context = {'form': form, 'user_type': user_type}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        form = SignUpForm(request.POST, user_type=user_type)
        if form.is_valid():
            user = form.save(user_type)
            login(self.request, user)
            return redirect('profile')
        else:
            context = {'form': form, 'user_type': user_type}
            return render(request, self.template_name, context)


def forbidden_view(request, user_type):
    next_page = request.GET.get('next')
    context = {'user_type': user_type, 'next_page': next_page}
    return render(request, 'forbidden.html', context=context)
