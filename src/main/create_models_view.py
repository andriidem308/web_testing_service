import json
import os.path
import random
from datetime import timedelta

import yaml
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from faker import Faker

from main.models import Group, Problem, Lecture
from main.services.logging_service import log_user
from main.services.users_service import get_teachers, create_student, create_teacher, get_students_by_group

User = get_user_model()


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

        teacher = create_teacher(user)
        teacher.save()

        log_user(teacher, password)

        response_log.append(f'Created teacher: {teacher}')

    return JsonResponse(response_log, safe=False)


def create_groups(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    group_names = config.get('group_names', [])

    teachers = get_teachers()

    for group_name in group_names:
        teacher = random.choice(teachers)
        group_name_full = f'{group_name} - 4'
        if not Group.objects.filter(name=group_name_full).exists():
            group = Group.objects.create(
                teacher=teacher,
                name=group_name_full
            )
            response_log.append(f'Created group: {group} with teacher {teacher}')

    return JsonResponse(response_log, safe=False)


def create_students(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    fake = Faker()

    max_students_per_group = config.get('max_students_per_group', 0)

    groups = Group.objects.all()

    for group in groups:
        current_amount_of_students = len(get_students_by_group(group) or [])
        if current_amount_of_students < max_students_per_group:
            students_amount_to_add = random.randint(1, max_students_per_group - current_amount_of_students)
            for _ in range(students_amount_to_add):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                username = email.split('@')[0]
                password = fake.password()

                if not (User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists()):
                    user = User.objects.create_student_user(username, email, password, first_name, last_name)
                    student = create_student(user, group)
                    student.save()

                    log_user(student, password)

                    response_log.append(f'Created student: {student} in group {group}')

    return JsonResponse(response_log, safe=False)


def create_problems(request):
    response_log = []
    problems_data = json.load(open('localtest/problems/problems_generator.json'))

    if not os.path.exists('media'):
        os.mkdir('media')
        response_log.append('Created media directory')

    if not os.path.exists('media/problems'):
        os.mkdir('media/problems')
        response_log.append('Created problems directory')

    if not os.path.exists('media/problems/test_files'):
        os.mkdir('media/problems/test_files')
        response_log.append('Created test_files directory')

    teachers = get_teachers()
    for teacher in teachers:
        groups = Group.objects.filter(teacher=teacher)

        for problem_data in problems_data:
            headline = problem_data.get('headline')
            content = problem_data.get('content')
            problem_value = random.randint(1, 10)
            max_exec_time = random.randrange(500, 5000, 500)
            time_now = timezone.now()
            random_days = timedelta(days=random.randint(0, 30))
            random_date = (time_now + random_days).replace(hour=0, minute=0, second=0, microsecond=0)

            headline_lower = headline.lower().replace(' ', '_')
            teacher_lower = str(teacher).lower().replace(' ', '_')
            test_filename = f'problems/test_files/{headline_lower}_{teacher_lower}.json'

            with open('media/' + test_filename, 'w') as tmp_test_file:
                tmp_test_file.write(json.dumps(problem_data.get('tests')))

            if not Problem.objects.filter(test_file=test_filename).exists():
                groups_amount = random.randint(0, len(groups))
                groups_selected = groups.order_by('?')[:groups_amount]
                problem = Problem.objects.create(
                    teacher=teacher,
                    headline=headline,
                    content=content,
                    max_points=problem_value,
                    max_execution_time=max_exec_time,
                    deadline=random_date,
                    date_created=time_now,
                    date_updated=time_now,
                    test_file=test_filename
                )
                problem.groups.set(groups_selected)

                response_log.append(f'Created problem: {headline} for groups {groups_selected} by teacher {teacher}')

    return JsonResponse(response_log, safe=False)


def create_lectures(request):
    response_log = []
    lectures_data = json.load(open('localtest/lectures/lectures_generator.json'))

    if not os.path.exists('media'):
        os.mkdir('media')
        response_log.append('Created media directory')

    if not os.path.exists('media/lectures'):
        os.mkdir('media/lectures')
        response_log.append('Created lectures directory')

    teachers = get_teachers()
    for teacher in teachers:
        groups = Group.objects.filter(teacher=teacher)

        for lecture_data in lectures_data:
            headline = lecture_data.get('headline')
            content = lecture_data.get('content')
            time_now = timezone.now()

            if not Lecture.objects.filter(headline=headline).filter(teacher=teacher).exists():
                groups_amount = random.randint(0, len(groups))
                groups_selected = groups.order_by('?')[:groups_amount]
                lecture = Lecture.objects.create(
                    teacher=teacher,
                    headline=headline,
                    content=content,
                    date_created=time_now,
                    date_updated=time_now,
                )
                lecture.groups.set(groups_selected)

                response_log.append(f'Created lecture: {headline} for groups {groups_selected} by teacher {teacher}')

    return JsonResponse(response_log, safe=False)


def create_all_models(request):
    response_log = []
    response_log.append(json.loads(create_teachers(request).content.decode()))
    response_log.append(json.loads(create_groups(request).content.decode()))
    response_log.append(json.loads(create_students(request).content.decode()))

    return JsonResponse(response_log, safe=False)
