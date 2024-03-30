from rest_framework import serializers

from main.models import Teacher, Student, Group, Article, Problem, Lecture, Solution, Comment

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        datatables_always_serialize = ('id', 'group', )


class ArticleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    groups = GroupSerializer()

    class Meta:
        model = Article
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    groups = GroupSerializer()

    class Meta:
        model = Problem
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'
