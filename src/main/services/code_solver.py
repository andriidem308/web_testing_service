import json
import os
import time
from subprocess import PIPE, Popen

from django.utils import timezone

from main.models import Solution
from main.services.notification_service import mail_student_take_problem_notify, create_problem_taken_notification
from core import settings


def read_json_s3(file_field):
    try:
        file_content = file_field.open(mode='r')
        file_content_str = file_content.read()
        return json.loads(file_content_str)

    except Exception as e:
        print("Error while reading test file on S3:", e)
        return None


def read_json_local(file_path):
    with open(file_path) as tests_file:
        return json.load(tests_file)


def test_student_solution(code, exec_time, tests):
    temporary_filename = 'test_solution.py'
    with open(temporary_filename, 'w') as temporary_file:
        temporary_file.write(code)

    successful_tests = 0
    total_tests = len(tests)

    for test in tests:
        test_inputs = test.get('inputs', [])
        test_outputs = test.get('outputs', [])

        command = [f'python3 {temporary_filename}']

        start_time = time.time()
        p = Popen(command, stdin=PIPE, stdout=PIPE, shell=True)
        shell_input = bytes('\n'.join(test_inputs), encoding='utf-8')
        buffer, buffer_err = p.communicate(input=shell_input)

        end_time = time.time()

        if (end_time - start_time) * 1000 <= exec_time:
            result_outputs = buffer.rstrip().decode('utf-8').split('\n')
            if result_outputs == test_outputs:
                successful_tests += 1

    score = successful_tests / total_tests

    os.remove(temporary_filename)

    return score


def problem_take(solution):
    current_time = timezone.now()

    problem = solution.problem

    problem_tests = []
    if settings.WORKFLOW == 's3':
        problem_tests = read_json_s3(problem.test_file)
    if settings.WORKFLOW == 'local':
        problem_tests = read_json_local(problem.test_file.path)

    score = test_student_solution(
        code=solution.solution_code,
        exec_time=solution.problem.max_execution_time,
        tests=problem_tests
    )

    if current_time > problem.deadline:
        score /= 2

    score = round(score, 2)

    previous_solution = Solution.objects.filter(student=solution.student).filter(problem=problem)
    if previous_solution:
        if score >= previous_solution[0].score:
            previous_solution.delete()
            solution.score = score
            solution.save()
            mail_student_take_problem_notify(solution)
            create_problem_taken_notification(solution)
    else:
        solution.score = score
        solution.save()
        mail_student_take_problem_notify(solution)
        create_problem_taken_notification(solution)
