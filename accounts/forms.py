import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from main.models import Student, Teacher, Group

User = get_user_model()


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        # 'autocomplete': 'off',
        'class': 'pretty-input',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # 'autocomplete': 'off',
        'class': 'pretty-input',
        'placeholder': 'Password',
    }))

    def clean(self):
        username = self.cleaned_data['username']
        if re.fullmatch('\w+@\w+\.\w\w+', username):
            user = User.objects.get(email=username)
            self.cleaned_data['username'] = user.username

        super().clean()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Name"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Surname'}),
                                max_length=32, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Username'}),
                               max_length=64, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'pretty-input', 'placeholder': 'E-mail'}),
                             max_length=64, label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Password'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Password confirmation'}), label='')

    secret_key = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Access key'}),
        label='', required=False)
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'pretty-input'}),
                                   queryset=Group.objects.all(), label='', empty_label='Select Group', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'group', 'secret_key')

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super(SignUpForm, self).__init__(*args, **kwargs)

        if user_type == 'teacher':
            self.fields['secret_key'].required = True
            self.fields['group'].widget = forms.HiddenInput()
        elif user_type == 'student':
            self.fields['group'].required = True
            self.fields['secret_key'].widget = forms.HiddenInput()

    @transaction.atomic
    def save(self, user_type, commit=True):
        user = super().save(commit=False)
        if user_type == 'student':
            user._is_student = True
            user.save()
            student = Student.objects.create(user=user, group=self.cleaned_data['group'])
        elif user_type == 'teacher':
            user._is_teacher = True
            user.save()
            teacher = Teacher.objects.create(user=user)

        return user
