from main.models import Teacher, Student


def get_teachers():
    return Teacher.objects.all()


def get_students():
    return Student.objects.all()


def create_teacher(user):
    return Teacher.objects.create(user=user)


def create_student(user, group):
    return Student.objects.create(user=user, group=group)


def get_teacher_user(user):
    teacher = None
    if Teacher.objects.filter(user=user).exists():
        teacher = Teacher.objects.get(user=user)
    return teacher


def get_student_user(user):
    student = None
    if Student.objects.filter(user=user).exists():
        student = Student.objects.get(user=user)
    return student


def get_teacher(request):
    user = request.user
    if user and user.is_authenticated:
        return get_teacher_user(user)
    return None


def get_student(request):
    user = request.user
    if user and user.is_authenticated:
        return get_student_user(user)
    return None


def get_group(user):
    student = get_student_user(user)
    if student:
        return student.group
    return None


def filter_common_queryset(queryset, request, show_all=False):
    result = queryset

    teacher = get_teacher(request)
    student = get_student(request)
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


def get_students_by_groups(groups):
    students = Student.objects.filter(group__in=groups)
    return students
