from django import forms
from django.utils import timezone

from main import models


class GroupCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=255,
                           widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Group Name"}))

    def __init__(self, teacher, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher

    class Meta:
        model = models.Group
        fields = ('name', )

    def save(self, **kwargs):
        instance = super(GroupCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        return instance


class GroupUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=255,
                           widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Group Name"}))

    class Meta:
        model = models.Group
        fields = ('name', )


class LectureCreateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    attachment = forms.FileField(required=False)

    def __init__(self, teacher, *args, **kwargs):
        super(LectureCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher
        self.fields['groups'].queryset = models.Group.objects.filter(teacher=self.teacher)

    class Meta:
        model = models.Lecture
        fields = ['headline', 'content', 'groups', 'attachment', ]

    def save(self, **kwargs):
        instance = super(LectureCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        self.save_m2m()
        return instance


class LectureUpdateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    attachment = forms.FileField()

    class Meta:
        model = models.Lecture
        fields = ['headline', 'content', 'groups', 'attachment', ]

    def __init__(self, *args, **kwargs):
        super(LectureUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['groups'].queryset = models.Group.objects.filter(teacher=self.instance.teacher)

    def save(self, **kwargs):
        instance = super(LectureUpdateForm, self).save(commit=False)
        instance.date_updated = timezone.now()
        instance.save()
        self.save_m2m()
        return instance


class TestCreateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    score = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'pretty-input', 'placeholder': ''}),
        required=False)

    def __init__(self, teacher, *args, **kwargs):
        super(TestCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher
        self.fields['groups'].queryset = models.Group.objects.filter(teacher=self.teacher)

    class Meta:
        model = models.Test
        fields = ['headline', 'content', 'groups', 'score']

    def save(self, **kwargs):
        commit = kwargs.pop('commit', True)
        instance = super(TestCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class TestUpdateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': "Headline"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = models.Test
        fields = ['headline', 'content', 'groups', ]

    def __init__(self, *args, **kwargs):
        super(TestUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['groups'].queryset = models.Group.objects.filter(teacher=self.instance.teacher)

    def save(self, **kwargs):
        instance = super(TestUpdateForm, self).save(commit=False)
        instance.date_updated = timezone.now()
        instance.save()
        self.save_m2m()
        return instance


class QuestionTakeForm(forms.ModelForm):
    answer_1 = forms.BooleanField(required=False)
    answer_2 = forms.BooleanField(required=False)
    answer_3 = forms.BooleanField(required=False)
    answer_4 = forms.BooleanField(required=False)

    def __init__(self, test_solution, question, *args, **kwargs):
        super(QuestionTakeForm, self).__init__(*args, **kwargs)
        self.test_solution = test_solution
        self.question = question

        self.fields['answer_1'].widget.attrs['id'] = f"{self.question.id}_answer_1"
        self.fields['answer_2'].widget.attrs['id'] = f"{self.question.id}_answer_2"
        self.fields['answer_3'].widget.attrs['id'] = f"{self.question.id}_answer_3"
        self.fields['answer_4'].widget.attrs['id'] = f"{self.question.id}_answer_4"

    class Meta:
        model = models.StudentAnswer
        fields = ['answer_1', 'answer_2', 'answer_3', 'answer_4']

    def save(self, **kwargs):
        instance = super(QuestionTakeForm, self).save(commit=False)
        instance.test_solution = self.test_solution
        instance.question = self.question
        instance.save()
        return instance

    def clean(self):
        super(QuestionTakeForm, self).clean()
        self.cleaned_data['answer_1'] = bool(self.data.get(f'{self.question.id}_answer_1'))
        self.cleaned_data['answer_2'] = bool(self.data.get(f'{self.question.id}_answer_2'))
        self.cleaned_data['answer_3'] = bool(self.data.get(f'{self.question.id}_answer_3'))
        self.cleaned_data['answer_4'] = bool(self.data.get(f'{self.question.id}_answer_4'))


class QuestionCreateForm(forms.ModelForm):
    content = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'pretty-input question-input', 'placeholder': 'Question'}))

    answer_1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'pretty-input'}))
    answer_2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'pretty-input'}))
    answer_3 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'pretty-input'}))
    answer_4 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'pretty-input'}))

    answer_1_correct = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    answer_2_correct = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    answer_3_correct = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    answer_4_correct = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = models.Question
        fields = ('content',
                  'answer_1', 'answer_1_correct',
                  'answer_2', 'answer_2_correct',
                  'answer_3', 'answer_3_correct',
                  'answer_4', 'answer_4_correct',)

    def __init__(self, test, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.test = test

    def save(self, **kwargs):
        instance = super(QuestionCreateForm, self).save(commit=False)
        instance.test = self.test
        instance.save()
        return instance


class ProblemCreateForm(forms.ModelForm):
    headline = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'pretty-input', 'placeholder': ""}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}))
    max_points = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'pretty-input', 'placeholder': ''}))
    max_execution_time = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'pretty-input', 'placeholder': '', 'min': 0, 'step': 100}))

    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            attrs={
                'autocomplete': 'off',
                'class': 'datetimeinput datetimepicker-input pretty-input',
                'data-target': '#id_deadline'
            },
        )
    )

    test_file = forms.FileField()

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def __init__(self, teacher, *args, **kwargs):
        super(ProblemCreateForm, self).__init__(*args, **kwargs)
        self.teacher = teacher
        self.fields['groups'].queryset = models.Group.objects.filter(teacher=self.teacher)

    class Meta:
        model = models.Problem
        fields = ['headline', 'content', 'max_points', 'max_execution_time', 'deadline', 'test_file', 'groups']

    def save(self, **kwargs):
        instance = super(ProblemCreateForm, self).save(commit=False)
        instance.teacher = self.teacher
        instance.save()
        self.save_m2m()
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
        widget=forms.DateTimeInput(
            attrs={
                'autocomplete': 'off',
                'class': 'datetimeinput datetimepicker-input pretty-input',
                'data-target': '#id_deadline'
            },
        )
    )

    test_file = forms.FileField()

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = models.Problem
        fields = ['headline', 'content', 'max_points', 'max_execution_time', 'deadline', 'test_file', 'groups']

    def __init__(self, *args, **kwargs):
        super(ProblemUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['groups'].queryset = models.Group.objects.filter(teacher=self.instance.teacher)

    def save(self, **kwargs):
        instance = super(ProblemUpdateForm, self).save(commit=False)
        instance.date_updated = timezone.now()
        instance.save()
        self.save_m2m()
        return instance


class ProblemTakeForm(forms.ModelForm):
    solution_code = forms.CharField(widget=forms.Textarea(attrs={'class': 'pretty-textarea'}), label='')

    def __init__(self, problem, student, *args, **kwargs):
        super(ProblemTakeForm, self).__init__(*args, **kwargs)
        self.problem = problem
        self.student = student

    class Meta:
        model = models.Solution
        fields = ['solution_code']


class CheckSolutionForm(forms.ModelForm):
    formatted_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'pretty-input', 'min': 0, 'step': 0.1}))

    class Meta:
        model = models.Solution
        fields = ['formatted_score']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'pretty-textarea', 'cols': '64', 'rows': '10'}),
        }
