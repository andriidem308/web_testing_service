from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._is_teacher = True

    class Meta:
        ordering = ('user__first_name', 'user__last_name',)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._student = True
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ('user__first_name', 'user__last_name',)

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
        problems = Problem.objects.filter(groups__in=[self.group])

        if problems:
            sum_score = sum(solution.score for solution in solutions) / len(problems)
        else:
            sum_score = 0

        return sum_score

    @property
    def problems_solved(self):
        solutions_amount = Solution.objects.filter(student=self).count()
        return solutions_amount


class Article(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)

    headline = models.CharField(max_length=255)
    content = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline


class Problem(Article):
    max_points = models.FloatField()
    max_execution_time = models.IntegerField()
    deadline = models.DateTimeField()

    test_file = models.FileField(upload_to='problems/test_files/', null=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    content = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.article} | {self.user.get_full_name()} | {self.date_created}'


class Solution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solution_code = models.TextField()
    score = models.FloatField()
    date_solved = models.DateTimeField(auto_now=True)
    checked = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['date_solved']

    def get_owner(self):
        return self.student

    def get_owner_name(self):
        return self.student.user.get_full_name()

    @property
    def points(self):
        return round(self.score * self.problem.max_points, 1)


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

    object_type = models.CharField(max_length=50, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)

    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


