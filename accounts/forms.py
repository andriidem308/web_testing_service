from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django_eolimp.settings import SECRET_KEY_TEACHER
from testing.models import Student, Teacher, Group


User = get_user_model()


class TeacherSignUpForm(UserCreationForm):
    pass

    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
    #                              max_length=32, label='')
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
    #                             max_length=32, label='')
    #
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
    #                          max_length=64, label='')
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    #                             label='')
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}), label='')
    #
    # secret_key = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Access code'}), label='')
    #
    # class Meta(UserCreationForm.Meta):
    #     model = User
    #     fields = ('first_name', 'last_name', 'email', 'secret_key',)
    #
    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user._teacher = True
    #     user.save()
    #     teacher = Teacher.objects.create(user=user)
    #     return user
    #
    # def clean(self):
    #     super().clean()
    #     secret_key = self.cleaned_data.get('secret_key')
    #     if secret_key:
    #         if secret_key != SECRET_KEY_TEACHER:
    #             raise forms.ValidationError(
    #                 'You must be a teacher to sign up as a teacher!',
    #                 code='password_mismatch',
    #             )


class StudentSignUpForm(UserCreationForm):
    pass
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
    #                              max_length=32, label='')
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
    #                             max_length=32, label='')
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
    #                          max_length=64, label='')
    #
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    #                             label='')
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}), label='')
    #
    # group = forms.ModelChoiceField(queryset=Group.objects.all(), label='', empty_label='Select Group')
    #
    # class Meta(UserCreationForm.Meta):
    #     model = User
    #     fields = ('first_name', 'last_name', 'email', 'group',)
    #
    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user._student = True
    #     user.save()
    #     student = Student.objects.create(user=user, group=self.cleaned_data['group'])
    #     return user
