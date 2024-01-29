from django.db import models

# from accounts.models import Student, Teacher
#
#
# class Group(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255, unique=True)
#
#     class Meta:
#         ordering = ('name', )
#
#     def __str__(self):
#         return self.name
#
#
# class Problem(models.Model):
#     pass
#     # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     # group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     #
#     # title = models.CharField(max_length=255)
#     # description = models.TextField()
#     #
#     # problem_value = models.FloatField()
#     # max_execution_time = models.FloatField()  # ms
#     #
#     # deadline = models.DateTimeField()
#     # date_created = models.DateTimeField(auto_now=True)
#     # date_updated = models.DateTimeField(auto_now=True)
#     #
#     # test_file = models.FileField(upload_to='files_uploaded/test_files/', null=True)
#     #
#     # class Meta:
#     #     ordering = ['-date_updated']
#
#
# class Solution(models.Model):
#     pass
#
#     # problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
#     # student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     # solution_code = models.TextField()
#     # score = models.FloatField()
#     # date_solved = models.DateTimeField(auto_now=True)
#     # checked = models.BooleanField(default=False, null=True)
#     #
#     # class Meta:
#     #     ordering = ['date_solved']
#     #
#     # def get_owner(self):
#     #     return self.student
#     #
#     # def get_owner_name(self):
#     #     return self.student.user.get_full_name()
#
#
# class Lecture(models.Model):
#     pass
#
#     # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     # group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     # title = models.CharField(max_length=255)
#     # description = models.TextField()
#     # date_created = models.DateTimeField(auto_now=True)
#     # date_updated = models.DateTimeField(auto_now=True)
#     # attachment = models.FileField(upload_to='files_uploaded/lectures_files', blank=True, null=True)
#     #
#     # class Meta:
#     #     ordering = ['-date_updated']
#     #
#     # def __str__(self):
#     #     return self.title

