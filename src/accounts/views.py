from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordChangeView as BasePasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from accounts import forms
from accounts import models
from main import models as models_main


@login_required
def profile(request):
    user: models.User = request.user
    if user.is_teacher:
        user_type = 'teacher'
        person = models_main.Teacher.objects.get(user=user)
    elif user.is_student:
        user_type = 'student'
        person = models_main.Student.objects.get(user=user)
    else:
        user_type = None
        person = None

    context = {'user': user, 'person': person, 'user_type': user_type}

    return render(request, 'accounts/profile.html', context=context)


class LoginView(BaseLoginView):
    model = models.User
    form_class = forms.AuthenticationForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')

        next_page = request.GET.get('next') or ''
        form = forms.AuthenticationForm()
        context = {'form': form, 'next_page': next_page}
        return render(request, self.template_name, context)


class SignUpView(CreateView):
    model = models.User
    form_class = forms.SignUpForm
    template_name = 'accounts/signup.html'

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
            print(form.errors)
            context = {'form': form, 'user_type': user_type}
            return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class PasswordChangeView(BasePasswordChangeView):
    form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'accounts/password_change.html'
