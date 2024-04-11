from django.http import JsonResponse
from rest_framework import viewsets, permissions

from api import serializers
from api.services import table_service
from main.models import Group, Teacher, Student, Article, Problem, Lecture, Comment, Solution, Test, TestSolution
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
        score = student.total_score
        tests = Test.objects.filter(groups__in=[student.group])
        problems = Problem.objects.filter(groups__in=[student.group])
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
    test_solutions = TestSolution.objects.filter(test=pk)

    print(test_solutions)

    # students = get_students_by_group(pk)
    # filtered_students = table_service.filter_students(request, students)
    # selected_students = table_service.select_students(request, filtered_students)
    #
    result = {
        'draw': request.GET.get('draw'),
        'recordsTotal': test_solutions.count(),
        'recordsFiltered': len(test_solutions),
        'data': [],
    }

    for i in range(4):
        for test_solution in test_solutions:

            first_name = test_solution.student.first_name
            last_name = test_solution.student.last_name

            result['data'].append({
                'student': f'{last_name} {first_name[:1]}.',
                'group': test_solution.student.group.name,
                'score': round(test_solution.score * test_solution.test.score, 3),
            })

    return JsonResponse(result, safe=False)
