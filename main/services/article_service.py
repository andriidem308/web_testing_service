from main.models import Problem, Lecture, Comment, Attachment, Teacher
from typing import List

from main.forms import CommentForm, AttachmentForm


def problem_all() -> List[Problem]:
    return Problem.objects.all()


def problem_find(problem_id: int) -> Problem:
    return Problem.objects.get(id=problem_id)


def lecture_all() -> List[Lecture]:
    return Lecture.objects.all()


def lecture_find(lecture_id: int) -> Lecture:
    return Problem.objects.get(id=lecture_id)


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


def comment_method(article, request):
    comments = Comment.objects.filter(article=article)

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


    # if request.method == 'POST':
    #
    #
    #     # A comment was posted
    #     comment_form = CommentsForm(data=request.POST)
    #     if comment_form.is_valid():
    #         # Create Comment object but don't save to database yet
    #         new_comment = comment_form.save(commit=False)
    #         # Assign the current post to the comment
    #         new_comment.post = post
    #         # Save the comment to the database
    #         new_comment.save()
    # else:
    #     comment_form = CommentsForm()
    # return comment_form, comments




