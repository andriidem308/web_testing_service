from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm, \
    PasswordChangeForm as BasePasswordChangeForm

from web_testing_service.settings import SECRET_KEY_TEACHER

from main.models import Student, Teacher, Group, Lecture, Problem

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

# ----------------------------------------------------------------


class GroupCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Group Name"}))

    def __init__(self, teacher, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher
        # for field in self.fields.values():
        #     field.label = ''

    class Meta:
        model = Group
        fields = ['name', ]

    def save(self, **kwargs):
        instance = super(GroupCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        return instance


class GroupUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=255,
                           widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Group Name"}))

    class Meta:
        model = Group
        fields = ['name', ]


class LectureCreateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    def __init__(self, teacher, *args, **kwargs):
        super(LectureCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher

    class Meta:
        model = Lecture
        fields = ['headline', 'content', ]

    def save(self, **kwargs):
        instance = super(LectureCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        return instance


class LectureUpdateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    class Meta:
        model = Lecture
        fields = ['headline', 'content', ]


class ProblemCreateForm(forms.ModelForm):
    pass


class ProblemUpdateForm(forms.ModelForm):
    pass
