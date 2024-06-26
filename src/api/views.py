from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api import serializers, permissions
from api.services import table_service
from main import models
from main.services.users_service import get_students_by_group


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.select_related('user').all()
    permission_classes = [AllowAny, ]
    serializer_class = serializers.TeacherSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = models.Group.objects.select_related('teacher').all()
    permission_classes = [permissions.TeacherOnly, ]
    serializer_class = serializers.GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.select_related('user', 'group').all()
    permission_classes = [AllowAny, ]
    serializer_class = serializers.StudentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.select_related('teacher').all()
    permission_classes = [permissions.IsTeacherOrReadOnly, ]
    serializer_class = serializers.ArticleSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = models.Problem.objects.select_related('teacher').all()
    permission_classes = [permissions.IsTeacherOrReadOnly, ]
    serializer_class = serializers.ProblemSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = models.Lecture.objects.select_related('teacher').all()
    permission_classes = [permissions.IsTeacherOrReadOnly, ]
    serializer_class = serializers.LectureSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.select_related('teacher').all()
    permission_classes = [permissions.IsTeacherOrReadOnly, ]
    serializer_class = serializers.TestSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.select_related('test').all()
    permission_classes = [permissions.IsTeacherOrReadOnly, ]
    serializer_class = serializers.QuestionSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.select_related('user', 'article').all()
    serializer_class = serializers.CommentSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.select_related('user', 'article').all()
    serializer_class = serializers.NotificationSerializer


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = models.Solution.objects.select_related('student', 'problem').all()
    permission_classes = [permissions.IsStudentOrReadOnly, ]
    serializer_class = serializers.SolutionSerializer


class TestSolutionViewSet(viewsets.ModelViewSet):
    queryset = models.TestSolution.objects.select_related('student', 'test').all()
    permission_classes = [permissions.IsStudentOrReadOnly, ]
    serializer_class = serializers.TestSolutionSerializer


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
        score = student.total_score
        tests = models.Test.objects.filter(groups__in=[student.group])
        problems = models.Problem.objects.filter(groups__in=[student.group])
        max_score = str(sum(problem.max_points for problem in problems) + sum(test.score for test in tests))
        max_score = max_score.replace('.0', '') if max_score.endswith('.0') else max_score

        result['data'].append({
            'first_name': table_service.highlight_search(student.first_name, request),
            'last_name': table_service.highlight_search(student.last_name, request),
            'score_percentage': f'{round(round(score, 3))} / {max_score}',
            'problems_solved': student.problems_solved,
            'tests_solved': student.tests_solved,
        })

    return JsonResponse(result, safe=False)


def test_solutions_data(request, pk):
    test_solutions = models.TestSolution.objects.filter(test=pk)

    ordered_solutions = table_service.order_solutions(request, test_solutions)

    result = {
        'draw': request.GET.get('draw'),
        'recordsTotal': test_solutions.count(),
        'recordsFiltered': len(test_solutions),
        'data': [],
    }

    for test_solution in ordered_solutions:
        first_name = test_solution.student.first_name
        last_name = test_solution.student.last_name

        result['data'].append({
            'student': f'{last_name} {first_name[:1]}.',
            'group': test_solution.student.group.name,
            'score': round(test_solution.score * test_solution.test.score, 3),
        })

    return JsonResponse(result, safe=False)
