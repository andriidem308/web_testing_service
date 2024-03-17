from django.core.mail import send_mail
from django.template.loader import render_to_string

from main.models import Student
from web_testing_service.settings import EMAIL_HOST_USER


def lecture_added_notify(lecture):
    teacher = lecture.teacher
    lecture_headline = lecture.headline
    groups = lecture.groups.all()

    #recipients = Student.objects.filter(group__in=groups)
    #recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New lecture "{lecture_headline}"'
    message = render_to_string('messages/lecture_add.html', {'lecture_title': lecture.headline, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)

    send_mail(subject, message, EMAIL_HOST_USER, recipients_email_list)

    print(recipients_email_list)


def problem_added_notify(problem):
    teacher = problem.teacher
    problem_headline = problem.headline
    groups = problem.groups.all()

    # recipients = Student.objects.filter(group__in=groups)
    # recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New problem "{problem_headline}"'
    message = render_to_string('messages/problem_add.html', {'problem_title': problem_headline, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)



# def test_added_notify(test):
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

def student_take_problem_notify(solution):
    student = solution.student
    problem_headline = solution.problem.headline
    teacher = solution.problem.teacher

    # teacher_email = teacher.user.email
    teacher_email = ""
    subject = f'New solution for problem "{problem_headline}" from {student}'
    message = render_to_string('messages/student_take_form.html', {'teacher': teacher, 'problem_title': problem_headline, 'student': student})
    send_mail(subject, '', EMAIL_HOST_USER, [teacher_email], html_message=message)