import json
import os
import time
from subprocess import PIPE, Popen


def test_student_solution(code, exec_time, test_filename):
    temporary_filename = 'test_solution.py'
    with open(temporary_filename, 'w') as temporary_file:
        temporary_file.write(code)

    with open(test_filename.path) as tests_file:
        tests = json.load(tests_file)
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
