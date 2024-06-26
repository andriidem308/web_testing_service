import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm as BaseAuthenticationForm, UserCreationForm,
                                       PasswordChangeForm as BasePasswordChangeForm)
from django.contrib.auth.password_validation import validate_password
from django.core.validators import ValidationError
from django.db import transaction

from core.settings import SECRET_KEY_TEACHER
from main.models import Group
from main.services.users_service import create_student, create_teacher

User = get_user_model()


def password_weak_validator(value):
    try:
        validate_password(value)
    except ValidationError as e:
        print(e)
        raise ValidationError('Password is too weak')


def secret_key_validator(value):
    if value:
        if value != SECRET_KEY_TEACHER:
            raise forms.ValidationError(
                'Invalid secret key',
                code='secret_key_mismatch',
            )
    else:
        raise forms.ValidationError(
            'Secret key is not entered',
            code='secret_key_mismatch',
        )


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'pretty-input', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'pretty-input', 'placeholder': 'Password'})
    )

    def clean(self):
        username = self.cleaned_data['username']
        if re.fullmatch(r'\w+@\w+\.\w\w+', username):
            user = User.objects.get(email=username)
            self.cleaned_data['username'] = user.username

        super().clean()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Name", 'autocomplete': 'off'}),
        max_length=32,
        label=''
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Surname', 'autocomplete': 'off'}),
        max_length=32,
        label=''
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': 'Username', 'autocomplete': 'off'}),
        max_length=64,
        label='',
        error_messages={'unique': 'User already exists'}
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'pretty-input', 'placeholder': 'E-mail', 'autocomplete': 'off'}),
        max_length=64,
        label=''
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Password', 'autocomplete': 'off'}),
        label='',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'pretty-input', 'placeholder': 'Password confirmation', 'autocomplete': 'off'}),
        label='',
        validators=[password_weak_validator],
    )

    secret_key = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'pretty-input', 'placeholder': 'Secret key', 'autocomplete': 'off'}),
        label='',
        required=False,
        validators=[secret_key_validator]
    )
    group = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'pretty-input'}), queryset=Group.objects.all(),
        label='',
        empty_label='Select Group',
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('group', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'secret_key')

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
            create_student(user, self.cleaned_data['group'])
        elif user_type == 'teacher':
            user._is_teacher = True
            user.save()
            create_teacher(user)

        return user


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'pretty-input',
            'placeholder': 'Old Password',
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'pretty-input',
            'placeholder': 'New Password',
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'pretty-input',
            'placeholder': 'Password Confirmation',
        })
    )
