from rest_framework import serializers

from .models import (AnswerGroup, AnswersStudent, AnswerTestTask,
                     BeforeUniversity, Chapter, Comment, Course, DataKnowledge,
                     DataKnowledgeFree, DataKnowledgeGeneral, File,
                     GroupStudent, Orders, Project, ProjectInvitation, Student,
                     StudentCV, StudentInvitation, TaskGroup, TaskStatusGroup,
                     TaskStatusStudent, TaskStudent, TestTask,
                     TestTaskEvaluation, UnderSection, University,
                     UserInterestsFirst, UserInterestsSecond,
                     UserInterestsThird)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class UserInterestsFirstSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestsFirst
        fields = '__all__'


class UserInterestsSecondSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestsSecond
        fields = '__all__'


class UserInterestsThirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestsThird
        fields = '__all__'


class BeforeUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BeforeUniversity
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCV
        fields = '__all__'


class StudentPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCV
        fields = '__all__'


class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        required=False
    )

    class Meta:
        model = Project
        fields = '__all__'

    def update(self, instance, validated_data):
        students = validated_data.pop('students', None)
        instance = super().update(instance, validated_data)

        if students is not None:
            instance.students.set(students)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AnswerTestTaskSerializer(serializers.ModelSerializer):
    tg_nickname = serializers.CharField(
        source='user.tg_nickname',
        read_only=True
    )

    class Meta:
        model = AnswerTestTask
        fields = '__all__'


class TestTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTask
        fields = '__all__'


class TestTaskEvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaskEvaluation
        fields = [
            'telegram_user_id', 'assigned_testtask', 'url',
            'score', 'is_completed', 'student'
        ]
        extra_kwargs = {
            'url': {'default': ''},
            'score': {'default': 0},
            'is_completed': {'default': 'No'}
        }

    def create(self, validated_data):
        telegram_user_id = validated_data.get('telegram_user_id')

        # Найти студента по telegram_user_id
        student = Student.objects.filter(
            telegram_user_id=telegram_user_id
        ).first()
        if not student:
            raise serializers.ValidationError(
                "Студент с таким Telegram ID не найден"
            )

        # Добавляем студента в validated_data
        validated_data['student'] = student
        return super().create(validated_data)


class TestTaskEvaluationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaskEvaluation
        fields = ['url']


class TestTaskEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaskEvaluation
        fields = '__all__'


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = '__all__'


class TaskStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStudent
        fields = '__all__'


class AnswerGroupSerializer(serializers.ModelSerializer):
    tg_nickname = serializers.CharField(
        source='user.tg_nickname',
        read_only=True
    )

    class Meta:
        model = AnswerGroup
        fields = '__all__'


class TaskStatusGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusGroup
        fields = '__all__'


class TaskStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStudent
        fields = '__all__'


class AnswersStudentSerializer(serializers.ModelSerializer):
    tg_nickname = serializers.CharField(
        source='user.tg_nickname',
        read_only=True
    )

    class Meta:
        model = AnswersStudent
        fields = '__all__'


class TaskStatusStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusStudent
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class UnderSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnderSection
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class DataKnowledgeSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    under_section = UnderSectionSerializer()
    files = FileSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = DataKnowledge
        fields = '__all__'


class DataKnowledgeFreeSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    under_section = UnderSectionSerializer()
    files = FileSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = DataKnowledgeFree
        fields = '__all__'


class DataKnowledgeFileSerializer(serializers.ModelSerializer):
    files = FileSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = DataKnowledge
        fields = '__all__'


class DataKnowledgeFreeFileSerializer(serializers.ModelSerializer):
    files = FileSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = DataKnowledgeFree
        fields = '__all__'


class DataKnowledgeGeneralSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()
    under_section = UnderSectionSerializer()
    files = FileSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = DataKnowledgeGeneral
        fields = '__all__'


class SubscriptionEndDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['subscription_end_date']


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class ProjectInvitationSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all()
    )

    class Meta:
        model = ProjectInvitation
        fields = '__all__'


class StudentInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInvitation
        fields = '__all__'
