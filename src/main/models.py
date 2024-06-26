from django.db import models

from accounts.models import User


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')
    user._is_teacher = True

    class Meta:
        ordering = ('user__first_name', 'user__last_name',)
        indexes = [
            models.Index(fields=['user',]),
        ]

    def __str__(self):
        return self.user.get_full_name()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['teacher']),
        ]

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    user._student = True
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')

    class Meta:
        ordering = ('user__first_name', 'user__last_name',)
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['group']),
        ]

    def __str__(self):
        return self.user.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    @property
    def group_name(self):
        return self.group.name

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def total_score(self):
        solutions = Solution.objects.filter(student=self)
        test_solutions = TestSolution.objects.filter(student=self)
        sum_score = 0
        sum_score += sum(solution.score * solution.problem.max_points for solution in solutions)
        sum_score += sum(test_solution.score * test_solution.test.score for test_solution in test_solutions)
        return sum_score

    @property
    def total_score_percentage(self):
        sum_score = self.total_score
        tests = Test.objects.filter(groups__in=[self.group])
        problems = Problem.objects.filter(groups__in=[self.group])

        if problems and tests:
            sum_score /= len(problems) + len(tests)
        elif problems:
            sum_score /= len(problems)
        elif tests:
            sum_score /= len(tests)

        return sum_score

    @property
    def problems_solved(self):
        solutions_amount = Solution.objects.filter(student=self).count()
        return solutions_amount

    @property
    def tests_solved(self):
        test_solutions_amount = TestSolution.objects.filter(student=self).count()
        return test_solutions_amount


class Article(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)

    headline = models.CharField(max_length=255)
    content = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

    class Meta:
        indexes = [
            models.Index(fields=['headline']),
            models.Index(fields=['content']),
            models.Index(fields=['teacher']),
        ]


class Problem(Article):
    max_points = models.FloatField()
    max_execution_time = models.IntegerField()
    deadline = models.DateTimeField()

    test_file = models.FileField(upload_to='problems/test_files/', null=True)

    class Meta:
        indexes = [
            models.Index(fields=['max_points'])
        ]

    @property
    def filename(self):
        return str(self.test_file).split('/')[-1]

    @property
    def file_url(self):
        return self.test_file.url


class Lecture(Article):
    attachment = models.FileField(upload_to='lectures/attachments/', null=True, blank=True)

    @property
    def filename(self):
        return str(self.attachment).split('/')[-1]

    @property
    def file_url(self):
        return self.attachment.url


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['article']),
        ]

    def __str__(self):
        return f'{self.article} | {self.user.get_full_name()} | {self.date_created}'


class Solution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='solutions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solutions')
    solution_code = models.TextField()
    score = models.FloatField()
    date_solved = models.DateTimeField(auto_now=True)
    checked = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['date_solved']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['problem']),
            models.Index(fields=['score']),
            models.Index(fields=['checked']),
        ]

    def get_owner(self):
        return self.student

    def get_owner_name(self):
        return self.student.user.get_full_name()

    @property
    def points(self):
        return round(self.score * self.problem.max_points, 1)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)

    object_type = models.CharField(max_length=50, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)

    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['object_type']),
            models.Index(fields=['is_seen']),
        ]


class Test(Article):
    score = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['score']),
        ]


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    answer_1 = models.CharField(max_length=255)
    answer_2 = models.CharField(max_length=255)
    answer_3 = models.CharField(max_length=255)
    answer_4 = models.CharField(max_length=255)

    answer_1_correct = models.BooleanField(default=False)
    answer_2_correct = models.BooleanField(default=False)
    answer_3_correct = models.BooleanField(default=False)
    answer_4_correct = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['test']),
        ]

    def __str__(self):
        return self.content

    @property
    def answers(self):
        return [self.answer_1, self.answer_2, self.answer_3, self.answer_4]

    @property
    def correct_answers(self):
        correct_answers = []
        if self.answer_1_correct:
            correct_answers.append(self.answer_1)
        if self.answer_2_correct:
            correct_answers.append(self.answer_2)
        if self.answer_3_correct:
            correct_answers.append(self.answer_3)
        if self.answer_4_correct:
            correct_answers.append(self.answer_4)
        return correct_answers


class TestSolution(models.Model):
    test = models.ForeignKey(Test, related_name='solutions', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        unique_together = ('test', 'student',)
        indexes = [
            models.Index(fields=['test']),
            models.Index(fields=['student']),
            models.Index(fields=['score']),
        ]

    @property
    def points(self):
        return round(self.score * self.test.score, 1)


class StudentAnswer(models.Model):
    test_solution = models.ForeignKey(TestSolution, related_name='student_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='student_answers', on_delete=models.CASCADE)

    answer_1 = models.BooleanField(default=False)
    answer_2 = models.BooleanField(default=False)
    answer_3 = models.BooleanField(default=False)
    answer_4 = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['test_solution']),
            models.Index(fields=['question']),
        ]
