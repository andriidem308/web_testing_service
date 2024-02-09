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


def get_students_by_group(group):
    students = Student.objects.filter(group=group)
    return students
