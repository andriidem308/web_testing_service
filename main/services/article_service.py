from main.models import Problem, Lecture
from typing import List


def problem_all() -> List[Problem]:
    return Problem.objects.all()


def problem_find(problem_id: int) -> Problem:
    return Problem.objects.get(id=problem_id)


def lecture_all() -> List[Lecture]:
    return Lecture.objects.all()


def lecture_find(lecture_id: int) -> Lecture:
    return Problem.objects.get(id=lecture_id)



