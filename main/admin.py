from django.contrib import admin

from main.models import Student, Teacher, Group


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Group)
