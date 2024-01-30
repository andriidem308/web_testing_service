from django import forms

from main.models import Lecture, Group, Problem
from main.utils.widget import TimePicker


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


# TODO: Problem forms

class ProblemCreateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))
    # max_points = forms.FloatField(widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Max points"}))
    # max_execution_time = forms.FloatField(widget=forms.TextInput(
    #     attrs={'class': 'pretty-input', 'placeholder': "Max execution time"}))
    max_points = forms.FloatField(widget=forms.NumberInput())
    max_execution_time = forms.FloatField(widget=forms.NumberInput())

    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=TimePicker(attrs={'autocomplete': 'off'})
    )

    def __init__(self, teacher, *args, **kwargs):
        super(ProblemCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher

    class Meta:
        model = Problem
        fields = ['headline', 'content', 'max_points', 'max_execution_time', 'deadline',]

    def save(self, **kwargs):
        instance = super(ProblemCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        return instance


class ProblemUpdateForm(forms.ModelForm):
    pass
