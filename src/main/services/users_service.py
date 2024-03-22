from main.models import Teacher, Student


def get_teacher(user):
    teacher = Teacher.objects.filter(user=user) or None
    if teacher:
        teacher = teacher[0]
    return teacher


def get_student(user):
    student = Student.objects.filter(user=user) or None
    if student:
        student = student[0]
    return student


def get_group(user):
    group = None
    if user.is_student:
        student = get_student(user)
        if student:
            group = student.group

    return group


def filter_common_queryset(queryset, user, show_all=False):
    result = queryset

    teacher = get_teacher(user)
    student = get_student(user)
    if teacher:
        if show_all == '1':
            result = queryset
        else:
            result = queryset.filter(teacher=teacher)
    elif student:
        result = queryset.filter(groups__in=[student.group])

    return result



def get_students_by_group(group):
    students = Student.objects.filter(group=group)
    return students
