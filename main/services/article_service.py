from main.models import Problem, Lecture, Comment, Attachment, Teacher, Solution
from typing import List

from main.forms import CommentForm, AttachmentForm


def problem_all() -> List[Problem]:
    return Problem.objects.all()


def problems_by_teacher(teacher) -> Lecture:
    return Problem.objects.filter(teacher=teacher)


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


def lecture_all() -> List[Lecture]:
    return Lecture.objects.all()


def lectures_by_teacher(teacher) -> List[Lecture]:
    return Lecture.objects.filter(teacher=teacher)


def lecture_find(lecture_id: int) -> Lecture:
    lecture = Lecture.objects.filter(id=lecture_id) or []
    if lecture:
        lecture = lecture[0]
    return lecture


def attachment_method(article, request):
    attachments = Attachment.objects.filter(article=article)
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        attachment_form = AttachmentForm(teacher=teacher, data=request.POST)
        if attachment_form.is_valid():
            new_attachment: Attachment = attachment_form.save(commit=False)
            new_attachment.article = article
            new_attachment.teacher = Teacher.objects.get(user=request.user)
            new_attachment.save()
    else:
        attachment_form = AttachmentForm(teacher=teacher)
    return attachment_form, attachments


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
    else:
        comment_form = CommentForm()
    return comment_form, comments
