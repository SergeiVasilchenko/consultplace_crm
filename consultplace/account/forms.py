# from modeltranslation.forms import TranslationModelForm
from account.models import (AnswerGroup, AnswersStudent, AnswerTestTask,
                            BeforeUniversity, Chapter, Comment, Course,
                            CustomUser, DataKnowledgeGeneral, GroupStudent,
                            Mailing, Orders, Project, ProjectInvitation,
                            Student, StudentCV, StudentInvitation,
                            StudentPortfolio, Subscription, TaskGroup,
                            TaskStatusGroup, TaskStatusStudent, TaskStudent,
                            TestTask, TestTaskEvaluation, UnderSection,
                            University, UserInterestsFirst,
                            UserInterestsSecond, UserInterestsThird)
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.forms import SelectMultiple
from django.utils.translation import gettext_lazy as _

from .models import (BOOLEAN_CHOICES, EDUCATION_STATUSES, MANAGER_STATUSES,
                     SPECIALIST_POSITIONS)


class StudentFilterForm(forms.Form):
    before_university = forms.ModelChoiceField(
        queryset=BeforeUniversity.objects.all(),
        empty_label=_("Образование"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        empty_label=_("Все университеты"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        empty_label=_("Все курсы"),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    manager_status = forms.ChoiceField(
        choices=MANAGER_STATUSES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    education_status = forms.ChoiceField(
        choices=EDUCATION_STATUSES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    position = forms.ChoiceField(
        choices=SPECIALIST_POSITIONS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class MailingForm(forms.ModelForm):
    subject = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Тема')
            }
        )
    )
    title = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Заголовок')
            }
        )
    )
    message = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('Сообщение')
            }
        )
    )
    photo = forms.ImageField(
        label=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        ),
        required=False
    )

    class Meta:
        model = Mailing
        fields = ['subject', 'title', 'message', 'photo']


class UserInterestsFirstForm(forms.ModelForm):
    class Meta:
        model = UserInterestsFirst
        fields = ('interest',)


class UserInterestsSecondForm(forms.ModelForm):
    class Meta:
        model = UserInterestsSecond
        fields = ('interest',)


class UserInterestsThirdForm(forms.ModelForm):
    class Meta:
        model = UserInterestsThird
        fields = ('interest',)


class BeforeUniversityForm(forms.ModelForm):
    class Meta:
        model = BeforeUniversity
        fields = ('name',)


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ('name',)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name',)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'position', 'full_name', 'groups'
        )

    proups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'password', 'is_superuser', 'username', 'email', 'is_staff',
            'is_busy', 'position', 'full_name', 'hours_per_week', 'groups'
        )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'full_name', 'mobile_phone', 'email', 'tg_nickname',
            'age', 'gender', 'before_university', 'university',
            'faculty', 'course',
            'interest_first', 'other_interest_first',
            'interest_second', 'other_interest_second',
            'interest_third', 'other_interest_third',
            'manager_status', 'education_status', 'hours_per_week',
            'telegram_user_id', 'subscription_end_date', 'position'
        )


class StudentCVForm(forms.ModelForm):
    class Meta:
        model = StudentCV
        fields = ('student', 'file')


class StudentPortfolioForm(forms.ModelForm):
    class Meta:
        model = StudentPortfolio
        fields = ('student', 'file')


class GroupStudentForm(forms.ModelForm):
    class Meta:
        model = GroupStudent
        fields = ('name', 'captain', 'students')


# форма для размещения в списке студентов для выбора проекта,
# на который надо пригласить студента
class ProjectSelectForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
        label="Select Project"
    )


class ProjectForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=SelectMultiple,
        required=False,
        label='Специалисты'
    )
    # chapter = forms.ModelChoiceField(
    #     queryset=DataKnowledgeGeneral.objects.all(),
    #     label='Тема базы знаний'
    # )
    pinned_dataknowledge = forms.ModelMultipleChoiceField(
        queryset=DataKnowledgeGeneral.objects.all(),
        widget=SelectMultiple,
        required=False,
        label='Методология'
    )

    class Meta:
        model = Project
        fields = (
            'students', 'name',
            'intricacy', 'start_date',
            'end_date', 'group_grade',
            'intricacy_coefficient',
            'pinned_dataknowledge', 'captain'
        )

    # def save(self, commit=True):
    #     project = super(). save(commit=False)
    #     data_knowledge_chapter = DataKnowledgeGeneral(
    #         chapter=self.cleaned_data['chapter']
    #     )
    #     if commit:
    #         project.save()
    #         data_knowledge_chapter.save()
    #     return project


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'project', 'user', 'student', 'comment_text'
        )


class TestTaskForm(forms.ModelForm):
    class Meta:
        model = TestTask
        fields = (
            'title', 'description', 'url',
            'task_duration'
        )


class AnswerTestTaskForm(forms.ModelForm):
    class Meta:
        model = AnswerTestTask
        fields = (
            'file', 'url', 'answer', 'user'
        )


class TaskGroupForm(forms.ModelForm):
    class Meta:
        model = TaskGroup
        fields = (
            'project', 'description',
            'project_cost', 'start_date',
            'end_date', 'grade'
        )


class AnswerGroupForm(forms.ModelForm):
    class Meta:
        model = AnswerGroup
        fields = ('file', 'url', 'answer', 'user')


class TaskStatusGroupForm(forms.ModelForm):
    class Meta:
        model = TaskStatusGroup
        fields = ('task_group', 'status')


class TaskStudentForm(forms.ModelForm):
    pinned_dataknowledge = forms.ModelMultipleChoiceField(
        queryset=DataKnowledgeGeneral.objects.all(),
        widget=SelectMultiple,
        required=False,
        label='Методология'
    )

    class Meta:
        model = TaskStudent
        fields = (
            'project', 'assigned_student', 'description',
            'title', 'project_cost', 'start_date', 'end_date',
            'pinned_dataknowledge', 'notice', 'material',
            'status', 'created_at'
        )


class AnswersStudentForm(forms.ModelForm):
    class Meta:
        model = AnswersStudent
        fields = (
            'file', 'url', 'comment', 'status',
            'task', 'personal_grade',
            'deadline_compliance', 'manager_recommendation',
            'intricacy_coefficient', 'task_credits', 'created_at'
        )


class TaskStatusStudentForm(forms.ModelForm):
    class Meta:
        model = TaskStatusStudent
        fields = ('task_student', 'status')


class TestTaskEvaluationForm(forms.ModelForm):
    is_completed = forms.ChoiceField(
        choices=BOOLEAN_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TestTaskEvaluation
        fields = (
            'student', 'url', 'score',
            'comment', 'assigned_testtask', 'is_completed', 'telegram_user_id'
        )


class DataKnowledgeGeneralForm(forms.ModelForm):
    class Meta:
        model = DataKnowledgeGeneral
        fields = (
            'chapter', 'under_section',
            'files', 'video_url', 'url'
        )


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('name',)


class UnderSectionForm(forms.ModelForm):
    class Meta:
        model = UnderSection
        fields = ('name',)


class MailingTranslationForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('subject', 'title', 'message', 'photo', 'student')


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'


class SubscriptionForm(forms.ModelForm):
    # user = forms.ModelChoiceField(
    #     queryset=Student.objects.all(),
    #     widget=forms.Select,
    #     required=True,
    #     label='Пользователь'
    # )

    class Meta:
        model = Subscription
        fields = '__all__'

    # def clean_user(self):
    #     user = self.cleaned_data['user']
    #     if user.subscription:
    #         raise forms.ValidationError('У этого студента уже есть подписка')
    #     return user


class ProjectInvitationForm(forms.ModelForm):
    class Meta:
        model = ProjectInvitation
        fields = '__all__'


class StudentInvitationForm(forms.ModelForm):
    class Meta:
        model = StudentInvitation
        fields = '__all__'
