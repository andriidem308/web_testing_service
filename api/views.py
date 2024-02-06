from rest_framework import viewsets, permissions

from api.serializers import GroupSerializer, TeacherSerializer, StudentSerializer, ArticleSerializer, ProblemSerializer, \
    LectureSerializer, AttachmentSerializer, TestFileSerializer, CommentSerializer, SolutionSerializer
from main.models import Group, Teacher, Student, Article, Problem, Lecture, Attachment, TestFile, Comment, Solution


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = TeacherSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'group').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = StudentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ArticleSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ProblemSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.select_related('teacher').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = LectureSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related('teacher', 'article').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AttachmentSerializer


class TestFileViewSet(viewsets.ModelViewSet):
    queryset = TestFile.objects.select_related('student', 'problem').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = TestFileSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'article').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CommentSerializer


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.select_related('student', 'problem').all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = SolutionSerializer
