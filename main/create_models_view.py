import json
import random

import yaml
from django.contrib.auth import get_user_model
from django.shortcuts import render
from faker import Faker
from django.http import JsonResponse, HttpResponse

from main.models import Teacher, Student, Group
from main.services.logging_service import log_user

User = get_user_model()


def index(request):
    return HttpResponse('<h1>Hello!</h1>')


def create_teachers(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    fake = Faker()

    number_of_teachers = config.get('number_of_teachers', 0)

    for _ in range(number_of_teachers):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = email.split('@')[0]
        password = fake.password()

        user = User.objects.create_teacher_user(username, email, password, first_name, last_name)

        teacher = Teacher.objects.create(user=user)
        teacher.save()

        log_user(teacher, password)

        response_log.append(f'Created teacher: {teacher}')

    return JsonResponse(response_log, safe=False)


def create_groups(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    group_names = config.get('group_names', [])

    teachers = Teacher.objects.all()

    for group_name in group_names:
        teacher = random.choice(teachers)
        group_name_full = f'{group_name} - 2'
        if not Group.objects.filter(name=group_name_full).exists():
            group = Group.objects.create(
                teacher=teacher,
                name=group_name_full
            )
            response_log.append(f'Created group: {group} with teacher {teacher}')

        # for year in range(1, 5):
        #     teacher = random.choice(teachers)
        #     group_name_full = f'{group_name}-{year}'
        #     if not Group.objects.filter(name=group_name_full).exists():
        #         group = Group.objects.create(
        #             teacher=teacher,
        #             name=group_name_full
        #         )
        #         response_log.append(f'Created group: {group} with teacher {teacher}')

    return JsonResponse(response_log, safe=False)


def create_students(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    fake = Faker()

    max_students_per_group = config.get('max_students_per_group', 0)

    groups = Group.objects.all()

    for group in groups:
        current_amount_of_students = len(Student.objects.filter(group=group) or [])
        if current_amount_of_students < max_students_per_group:
            students_amount_to_add = random.randint(1, max_students_per_group - current_amount_of_students)
            for _ in range(students_amount_to_add):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                username = email.split('@')[0]
                password = fake.password()

                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_student_user(username, email, password, first_name, last_name)
                    student = Student.objects.create(user=user, group=group)
                    student.save()

                    log_user(student, password)

                    response_log.append(f'Created student: {student} in group {group}')

    return JsonResponse(response_log, safe=False)



def create_all_models(request):
    response_log = []
    response_log.append(json.loads(create_teachers(request).content.decode()))
    response_log.append(json.loads(create_groups(request).content.decode()))
    response_log.append(json.loads(create_students(request).content.decode()))

    return JsonResponse(response_log, safe=False)
