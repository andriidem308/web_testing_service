from django.core.mail import send_mail
from django.template.loader import render_to_string


from web_testing_service.settings import EMAIL_HOST_USER


def lecture_added_notify(lecture):
    teacher = lecture.teacher
    lecture_headline = lecture.headline
    groups = lecture.groups

    # recipients = Student.objects.filter(group__in=groups)
    # recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New lecture "{lecture_headline}"'
    message = render_to_string('messages/lecture_add.html', {'lecture_title': lecture.headline, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)

    send_mail(subject, message, EMAIL_HOST_USER, recipients_email_list)

    print(recipients_email_list)


def problem_added_notify(problem):
    teacher = problem.teacher
    problem_headline = problem.headline
    groups = problem.groups

    # recipients = Student.objects.filter(group__in=groups)
    # recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New problem "{problem_headline}"'
    message = render_to_string('messages/problem_add.html', {'problem_title': problem_headline, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)
