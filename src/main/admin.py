from django.contrib import admin

from main import models


admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Group)
admin.site.register(models.Problem)
admin.site.register(models.Solution)
admin.site.register(models.Lecture)
admin.site.register(models.Comment)
admin.site.register(models.Notification)
admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.TestSolution)
admin.site.register(models.StudentAnswer)
