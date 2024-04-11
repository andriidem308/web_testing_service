from typing import List

from main.forms import CommentForm
from main.models import Comment, Lecture, Problem, Solution, StudentAnswer
from main.services.notification_service import create_article_commented_notification


def problem_all() -> List[Problem]:
    return Problem.objects.all()


def problems_by_teacher(teacher) -> List[Problem]:
    return Problem.objects.filter(teacher=teacher)


def problems_by_group(group) -> List[Problem]:
    return Problem.objects.filter(group=group)


def problem_find(problem_id: int) -> Problem:
    problem = Problem.objects.filter(id=problem_id) or []
    if problem:
        problem = problem[0]
    return problem


def solution_find(problem, student):
    solution = Solution.objects.filter(student=student, problem=problem.id) or []
    if solution:
        solution = solution[0]
    return solution


def solutions_by_student(student):
    solutions = Solution.objects.filter(student=student)
    return solutions


def solutions_by_problem(problem):
    solutions = Solution.objects.filter(problem=problem).order_by('checked', '-date_solved')
    return solutions


def solutions_unchecked_by_problem(problem):
    solutions = Solution.objects.filter(problem=problem, checked=False).order_by('date_solved')
    return solutions


def lecture_all() -> List[Lecture]:
    return Lecture.objects.all()


def lectures_by_teacher(teacher) -> List[Lecture]:
    return Lecture.objects.filter(teacher=teacher)


def lecture_find(lecture_id: int) -> Lecture:
    lecture = Lecture.objects.filter(id=lecture_id) or []
    if lecture:
        lecture = lecture[0]
    return lecture


def get_comments(article):
    comments = Comment.objects.filter(article=article).order_by('-date_created')
    return comments


def comment_method(article, request):
    comments = Comment.objects.filter(article=article).order_by('-date_created')

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment: Comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            create_article_commented_notification(new_comment)
    else:
        comment_form = CommentForm()
    return comment_form, comments


def student_answer_find(test, student):
    student_answer = StudentAnswer.objects.filter(student=student, test=test.id)
    if student_answer:
        student_answer = student_answer[0]
    return student_answer
