from main.models import Notification, Problem, Student

mail_notifications_types = ('problem', 'problem', 'problem', 'solution')


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


def create_new_lecture_notification():
    pass


def create_new_test_notification():
    pass


def create_solution_checked_notification():
    pass


def create_problem_taken_notification():
    pass


def create_article_commented_notification():
    pass

