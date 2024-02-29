from django.http import JsonResponse
from rest_framework import viewsets, permissions

from api import serializers
from api.services import table_service
from main.models import Group, Teacher, Student, Article, Problem, Lecture, Attachment, Comment, Solution
from main.services.users_service import get_students_by_group


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.TeacherSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'group').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.StudentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.ArticleSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.ProblemSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.LectureSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related('teacher', 'article').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.AttachmentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'article').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.CommentSerializer


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.select_related('student', 'problem').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.SolutionSerializer


def group_data(request, pk):
    students = get_students_by_group(pk)
    filtered_students = table_service.filter_students(request, students)
    selected_students = table_service.select_students(request, filtered_students)

    result = {
        'draw': request.GET.get('draw'),
        'recordsTotal': students.count(),
        'recordsFiltered': len(filtered_students),
        'data': [],
    }

    for student in selected_students:
        result['data'].append({
            'first_name': table_service.highlight_search(student.first_name, request),
            'last_name': table_service.highlight_search(student.last_name, request),
            'score_percentage': f'{round(student.total_score, 3) * 100}%',
            'problems_solved': student.problems_solved,
        })

    return JsonResponse(result, safe=False)


def solutions_data(request, pk):
    students = get_students_by_group(pk)
    filtered_students = table_service.filter_students(request, students)
    selected_students = table_service.select_students(request, filtered_students)

    result = {
        'draw': request.GET.get('draw'),
        'recordsTotal': students.count(),
        'recordsFiltered': len(filtered_students),
        'data': [],
    }

    for student in selected_students:
        result['data'].append({
            'first_name': table_service.highlight_search(student.first_name, request),
            'last_name': table_service.highlight_search(student.last_name, request),
            'score_percentage': f'{round(student.total_score, 3) * 100}%',
            'problems_solved': student.problems_solved,
        })

    return JsonResponse(result, safe=False)
