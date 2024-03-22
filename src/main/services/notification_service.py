from django.core.mail import send_mail
from django.template.loader import render_to_string

from main.models import Notification, Student
from core.settings import EMAIL_HOST_USER

mail_notifications_types = ('problem', 'problem', 'problem', 'solution')


def mail_lecture_added_notify(lecture):
    teacher = lecture.teacher
    lecture_headline = lecture.headline
    groups = lecture.groups.all()

    #recipients = Student.objects.filter(group__in=groups)
    #recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = []

    subject = f'New lecture "{lecture_headline}"'
    message = render_to_string('messages/lecture_add.html', {'lecture_title': lecture.headline, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)



def mail_problem_added_notify(problem):
    teacher = problem.teacher
    problem_headline = problem.headline
    groups = problem.groups.all()

    # recipients = Student.objects.filter(group__in=groups)
    # recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = []

    subject = f'New problem "{problem_headline}"'
    message = render_to_string('messages/problem_add.html', {'problem_title': problem_headline, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)



# def mail_test_added_notify(test):
#     teacher = test.teacher
#     test_headline = test.headline
#     groups = test.groups.all()
#
#     # recipients = Student.objects.filter(group__in=groups)
#     # recipients_email_list = [recipient.user.email for recipient in recipients]
#     recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']
#
#     subject = f'New problem "{test_headline}"'
#     message = render_to_string('messages/test_add.html', {'test_title': test_headline, 'teacher': teacher})
#     send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)

def mail_student_take_problem_notify(solution):
    student = solution.student
    problem_headline = solution.problem.headline
    teacher = solution.problem.teacher

    # teacher_email = teacher.user.email
    teacher_email = ""
    subject = f'New solution for problem "{problem_headline}" from {student}'
    message = render_to_string('messages/student_take_form.html', {'teacher': teacher, 'problem_title': problem_headline, 'student': student})
    send_mail(subject, '', EMAIL_HOST_USER, [teacher_email], html_message=message)


def create_notification(user, message, object_type, object_id):
    notification = Notification.objects.create(user=user, message=message, object_type=object_type, object_id=object_id)
    if object_type in mail_notifications_types:
        # send email notification
        pass

    notification.save()


def create_new_problem_notifications(problem):
    groups = problem.groups.all()
    students = Student.objects.filter(group__in=groups)
    message = f'<b>{problem.teacher}</b> created a <b>new problem</b> "{problem}"'
    object_type = 'problem'
    for student in students:
        create_notification(student.user, message, object_type, problem.id)


def create_new_lecture_notification(lecture):
    groups = lecture.groups.all()
    students = Student.objects.filter(group__in=groups)
    message = f'<b>{lecture.teacher}</b> created a <b>new lecture</b> "{lecture}"'
    object_type = 'lecture'
    for student in students:
        create_notification(student.user, message, object_type, lecture.id)


# def create_new_test_notification(test):
#     groups = test.groups.all()
#     students = Student.objects.filter(group__in=groups)
#     message = f'<b>{test.teacher}</b> created a <b>new test</b> "{test}"'
#     object_type = 'test'
#     for student in students:
#         create_notification(student.user, message, object_type, test.id)


def create_solution_checked_notification(solution):
    problem_headline = solution.problem.headline
    student = solution.student
    message = f'<b>{solution.problem.teacher}</b> checked your solution of problem <b>"{problem_headline}"</b> '
    object_type = 'problem'
    create_notification(student.user, message, object_type, solution.problem.id)


def create_problem_taken_notification(solution):
    problem_headline = solution.problem.headline
    teacher = solution.problem.teacher
    message = f'<b>{solution.student}</b> take a problem <b>"{problem_headline}"</b> '
    object_type = 'solution'
    create_notification(teacher.user, message, object_type, solution.id)


def create_article_commented_notification():
    pass

