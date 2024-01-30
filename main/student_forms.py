from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from main.models import Student, Teacher, Group


User = get_user_model()


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
                                max_length=32, label='')
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                             max_length=64, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
                             max_length=64, label='')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}), label='')

    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='', empty_label='Select Group')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'group',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user._student = True
        user.save()
        student = Student.objects.create(user=user, group=self.cleaned_data['group'])
        return user
