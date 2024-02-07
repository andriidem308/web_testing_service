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
