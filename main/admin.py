from django.contrib import admin

from main.models import Student, Teacher, Group, Problem, Lecture, Attachment, Comment, Solution


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Lecture)
admin.site.register(Attachment)
admin.site.register(Comment)
