from django.contrib.auth import get_user_model
from rest_framework import serializers

from main import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Teacher
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = models.Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Student
        fields = '__all__'
        datatables_always_serialize = ('id', 'group',)


class ArticleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.Article
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lecture
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.Problem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ProblemSerializer, self).to_representation(instance)
        fields_to_pop = ['test_file', ]
        if not self.context['request'].user.is_teacher:
            [representation.pop(field, '') for field in fields_to_pop]
        return representation


class SolutionSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    problem = ProblemSerializer()

    class Meta:
        model = models.Solution
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(SolutionSerializer, self).to_representation(instance)
        fields_to_pop = ['solution_code', ]
        if not self.context['request'].user.is_teacher:
            [representation.pop(field, '') for field in fields_to_pop]
        return representation


class TestSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.Test
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    test = TestSerializer()

    class Meta:
        model = models.Question
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(QuestionSerializer, self).to_representation(instance)
        fields_to_pop = ['answer_1_correct', 'answer_2_correct', 'answer_3_correct', 'answer_4_correct']
        if not self.context['request'].user.is_teacher:
            [representation.pop(field, '') for field in fields_to_pop]
        return representation


class TestSolutionSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    student = StudentSerializer()

    class Meta:
        model = models.TestSolution
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    article = ArticleSerializer()

    class Meta:
        model = models.Comment
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Notification
        fields = '__all__'
