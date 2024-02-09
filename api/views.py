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
    search_value = request.GET.get('search[value]', '').strip()
    page_size = int(request.GET.get('length', 0))
    offset = int(request.GET.get('start', 0))

    students = get_students_by_group(pk)
    filtered_students = table_service.filter_students(request, students)
    selected_students = filtered_students[offset:offset + page_size]

    result = {
        'draw': request.GET.get('draw'),
        'recordsTotal': students.count(),
        'recordsFiltered': filtered_students.count(),
        'data': list(),
    }

    problems = Problem.objects.filter(groups__in=[pk])
    total_points = sum(problem.max_points for problem in problems)
    print(total_points)

    for student in selected_students:
        first_name = student.user.first_name
        last_name = student.user.last_name

        if search_value:
            first_name = table_service.highlight_search(first_name, search_value)
            last_name = table_service.highlight_search(last_name, search_value)

        solutions = Solution.objects.filter(student=student)
        points = sum(solution.score for solution in solutions)

        score_percentage = round(points / total_points * 100)

        result['data'].append({
            'first_name': first_name,
            'last_name': last_name,
            'score_percentage': f'{score_percentage}%',
            'problems_solved': f'{solutions.count()}/{problems.count()}',
        })

    return JsonResponse(result, safe=False)
