from django.core.mail import send_mail
from django.template.loader import render_to_string

from accounts.models import User
from core.settings import EMAIL_HOST_USER
from main.models import Notification
from main.services.users_service import get_students_by_groups


def mail_lecture_added_notify(lecture):
    teacher = lecture.teacher
    groups = lecture.groups.all()

    recipients = get_students_by_groups(groups)
    recipients_email_list = [recipient.user.email for recipient in recipients]

    subject = f'New lecture "{lecture.headline}"'
    context = {
        'teacher': teacher,
        'lecture': lecture,
    }

    message = render_to_string('messages/lecture_add.html', context=context)
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)


def mail_problem_added_notify(problem):
    teacher = problem.teacher
    groups = problem.groups.all()

    recipients = get_students_by_groups(groups)
    recipients_email_list = [recipient.user.email for recipient in recipients]

    subject = f'New problem "{problem.headline}"'
    context = {
        'teacher': teacher,
        'problem': problem,
    }

    message = render_to_string('messages/problem_add.html', context=context)
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)


def mail_test_added_notify(test):
    teacher = test.teacher
    groups = test.groups.all()

    recipients = get_students_by_groups(groups)
    recipients_email_list = [recipient.user.email for recipient in recipients]

    subject = f'New test "{test.headline}"'
    context = {
        'teacher': teacher,
        'test': test,
    }

    message = render_to_string('messages/test_add.html', context=context)
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)


def mail_student_take_problem_notify(solution):
    student = solution.student
    teacher = solution.problem.teacher

    teacher_email = teacher.user.email
    subject = f'New solution for problem "{solution.problem.headline}" from {student}'
    message = render_to_string(
        template_name='messages/student_take_form.html',
        context={'teacher': teacher, 'student': student, 'solution': solution}
    )
    send_mail(subject, '', EMAIL_HOST_USER, [teacher_email], html_message=message)


def create_notification(user, message, object_type, object_id):
    notification = Notification.objects.create(user=user, message=message, object_type=object_type, object_id=object_id)
    notification.save()


def create_new_problem_notifications(problem):
    groups = problem.groups.all()
    students = get_students_by_groups(groups)
    message = f'<b>{problem.teacher}</b> created a <b>new problem</b> "{problem}"'
    object_type = 'problem'
    for student in students:
        create_notification(student.user, message, object_type, problem.id)


def create_new_lecture_notification(lecture):
    groups = lecture.groups.all()
    students = get_students_by_groups(groups)
    message = f'<b>{lecture.teacher}</b> created a <b>new lecture</b> "{lecture}"'
    object_type = 'lecture'
    for student in students:
        create_notification(student.user, message, object_type, lecture.id)


def create_new_test_notification(test):
    groups = test.groups.all()
    students = get_students_by_groups(groups)
    message = f'<b>{test.teacher}</b> created a <b>new test</b> "{test}"'
    object_type = 'test'
    for student in students:
        create_notification(student.user, message, object_type, test.id)


def create_solution_checked_notification(solution):
    student = solution.student
    message = f'<b>{solution.problem.teacher}</b> checked your solution of problem <b>"{solution.problem.headline}"</b>'
    object_type = 'problem'
    create_notification(student.user, message, object_type, solution.problem.id)


def create_problem_taken_notification(solution):
    teacher = solution.problem.teacher
    message = f'<b>{solution.student}</b> solved the problem <b>"{solution.problem.headline}"</b> '
    object_type = 'solution'
    create_notification(teacher.user, message, object_type, solution.id)


def create_article_commented_notification(comment):
    user = comment.user
    groups = comment.article.groups.all()

    recipients = list(User.objects.filter(student__group__in=groups))
    recipients.append(comment.article.teacher.user)
    if user in recipients:
        recipients.remove(user)

    object_type = comment.article.__class__.__name__.lower()
    message = f'<b>{user}</b> left a comment on <b>"{comment.article.headline}"</b>'

    for recipient in recipients:
        create_notification(recipient, message, object_type, comment.article.id)
