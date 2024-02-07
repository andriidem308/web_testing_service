from django import forms
from django.utils import timezone

from main.models import Lecture, Group, Problem, Comment, Attachment, Solution
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


class ProblemCreateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))
    max_points = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'pretty-input', 'placeholder': 'Max points'}))
    max_execution_time = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'pretty-input', 'placeholder': 'Max execution time (ms)', 'min': 0, 'step': 100}))

    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=TimePicker(attrs={'autocomplete': 'off'})
    )

    test_file = forms.FileField()

    def __init__(self, teacher, *args, **kwargs):
        super(ProblemCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher

    class Meta:
        model = Problem
        fields = ['headline', 'content', 'max_points', 'max_execution_time', 'deadline', 'test_file']

    def save(self, **kwargs):
        instance = super(ProblemCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        return instance


class ProblemUpdateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    max_points = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'pretty-input', 'placeholder': 'Max points', 'min': 0}))
    max_execution_time = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'pretty-input', 'placeholder': 'Max execution time (ms)', 'min': 0, 'step': 100}))

    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=TimePicker(attrs={'autocomplete': 'off'})
    )

    class Meta:
        model = Problem
        fields = ['headline', 'content', 'max_points', 'max_execution_time', 'deadline', 'test_file']
        widgets = {
            'test_file': forms.TextInput(attrs={
                "type": "File",
                "class": "form-control",
                "style": "display: none;",
                'onchange': 'displayFileName()',
            })
        }

    def __init__(self, *args, **kwargs):
        super(ProblemUpdateForm, self).__init__(*args, **kwargs)
        print(args)
        print(kwargs)

        instance = kwargs.get('instance')
        if instance:
            print(instance.deadline)
            print(instance.test_file)
            print(instance.date_updated)

    def save(self, **kwargs):
        instance = super(ProblemUpdateForm, self).save(commit=False)
        instance.date_updated = timezone.now()
        print("--- test_file ---")
        print(instance.test_file)
        instance.save()
        return instance



class ProblemTakeForm(forms.ModelForm):
    solution_code = forms.CharField(widget=forms.Textarea(), label='')

    def __init__(self, problem, student, *args, **kwargs):
        super(ProblemTakeForm, self).__init__(*args, **kwargs)
        self.problem = problem
        self.student = student

    class Meta:
        model = Solution
        fields = ['solution_code']


class AttachmentForm(forms.ModelForm):

    def __init__(self, teacher, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.teacher = teacher

    class Meta:
        model = Attachment
        fields = ['content', ]
        widgets = {
            'content': forms.TextInput(attrs={
                "name": "images",
                "type": "File",
                "class": "form-control",
                "multiple": "True",
                "style": "display: none;",
                'onchange': 'displayFileName()',
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'pretty-textarea'}),
        }
