from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import User
from main.services.s3_helper import S3MediaStorage
from web_testing_service import settings


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._is_teacher = True

    class Meta:
        ordering = ('user__first_name', 'user__last_name',)

    def __str__(self):
        return self.user.get_full_name()


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

    def get_group(self):
        return self.group

    def get_group_name(self):
        return self.group.name


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

    if settings.workflow == 's3':
        test_file = models.FileField(upload_to='', storage=S3MediaStorage(), null=True)
    elif settings.workflow == 'local':
        test_file = models.FileField(upload_to='problems/test_files/', null=True)


class Lecture(Article):
    pass


class Attachment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    content = models.FileField(upload_to='media/lectures/attachments/')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)


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
