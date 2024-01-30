from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from web_testing_service.settings import SECRET_KEY_TEACHER
from main.models import Student, Teacher, Group


User = get_user_model()


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'First name'}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Last name'}),
                                max_length=32, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Username'}),
                               max_length=32, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'pretty-input', 'placeholder': 'Email'}),
                             max_length=64, label='')
    secret_key = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Access key'}),
                                 label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Password'}),
                                label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Password Confirmation'}),
                                label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'secret_key',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user._is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user

    def clean(self):
        super().clean()
        secret_key = self.cleaned_data.get('secret_key')
        if secret_key:
            if secret_key != SECRET_KEY_TEACHER:
                raise forms.ValidationError(
                    'You must be a teacher to sign up as a teacher!',
                    code='password_mismatch',
                )

