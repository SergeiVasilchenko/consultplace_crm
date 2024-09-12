from account.filters import (InterestFirstFilter, InterestSecondFilter,
                             InterestThirdFilter)
from account.forms import (  # DataKnowledgeForm, DataKnowledgeFreeForm,
    AnswerGroupForm, AnswersStudentForm, AnswerTestTaskForm,
    BeforeUniversityForm, ChapterForm, CommentForm, CourseForm,
    CustomUserChangeForm, CustomUserCreationForm, DataKnowledgeGeneralForm,
    GroupStudentForm, MailingTranslationForm, OrdersForm, ProjectForm,
    ProjectInvitationForm, ProjectSelectForm, StudentCVForm, StudentForm,
    StudentInvitationForm, StudentPortfolioForm, SubscriptionForm,
    TaskGroupForm, TaskStatusGroupForm, TaskStatusStudentForm, TaskStudentForm,
    TestTaskEvaluationForm, TestTaskForm, UnderSectionForm, UniversityForm,
    UserInterestsFirstForm, UserInterestsSecondForm, UserInterestsThirdForm)
from account.models import (AnswerGroup, AnswersStudent, AnswerTestTask,
                            BeforeUniversity, Chapter, Comment, Course,
                            CustomUser, DataKnowledge, DataKnowledgeFree,
                            DataKnowledgeGeneral, File, GroupStudent, Mailing,
                            Orders, Project, ProjectInvitation, Student,
                            StudentCV, StudentInvitation, StudentPortfolio,
                            Subscription, TaskGroup, TaskStatusGroup,
                            TaskStatusStudent, TaskStudent, TestTask,
                            TestTaskEvaluation, UnderSection, University,
                            UserInterestsFirst, UserInterestsSecond,
                            UserInterestsThird)
from django import forms
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Q
# from django.forms import inlineformset_factory
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class StudentCVInline(TabularInline):
    model = StudentCV
    extra = 1
    fk_name = 'student'
    form = StudentCVForm


class StudentPortfolioInline(TabularInline):
    model = StudentPortfolio
    extra = 1
    form = StudentPortfolioForm
    fk_name = 'student'


class MailingSelectionForm(forms.Form):
    mailing = forms.ModelChoiceField(
        queryset=Mailing.objects.all(),
        empty_label=None,  # Чтобы не было пустой опции
        widget=forms.Select(attrs={'class': 'form-control'})
    )


# кастовмное действие - приглашение студента в проект
@admin.action(description='Invite selected students to project')
def invite_students_to_project(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = ProjectSelectForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            invitation = ProjectInvitation.objects.create(project=project)
            for student in queryset:
                StudentInvitation.objects.create(
                    invitation=invitation,
                    student=student
                )
            modeladmin.message_user(request, "Students have been invited.")
            return
        else:
            # Обработка случая, когда форма невалидна
            modeladmin.message_user(
                request,
                "Invalid form submission",
                level="error"
            )
            return render(
                request,
                'admin/invite_students_to_project.html',
                context={'students': queryset, 'form': form}
            )

    else:
        form = ProjectSelectForm()

    return render(
        request,
        'admin/invite_students_to_project.html',
        context={'students': queryset, 'form': form}
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = (
        'full_name', 'university', 'course', 'hours_per_week',
        'projects_in_progress', 'tasks_in_progress',
        'calculate_total_credits', 'calculate_total_rating'
    )
    list_display_links = (
        'full_name', 'university', 'course', 'hours_per_week'
    )
    list_filter = (
        'university', 'before_university', 'course',
        InterestFirstFilter, InterestSecondFilter, InterestThirdFilter
        # TasksInProgressFilter, ProjectsInProgressFilter
    )
    readonly_fields = ('position',)
    search_fields = ('full_name', 'email', 'tg_nickname')
    actions = [invite_students_to_project]
    inlines = [StudentCVInline, StudentPortfolioInline]

    def get_queryset(self, request):
        # аннотация для сортировки агрегированных значений
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            # projects_in_progress_count=Count(
            #     'projects',
            #     filter=~Q(projects__tasks__status='finished'),
            #     distinct=True
            # ),
            projects_in_progress_count=Count(
                'assigned_tasks__project',
                filter=~Q(assigned_tasks__status='finished'),
                distinct=True
            ),
            tasks_in_progress_count=Count(
                'assigned_tasks',
                filter=~Q(assigned_tasks__status='finished')
            )
        )
        return queryset

    def projects_in_progress(self, obj):
        return obj.projects_in_progress_count
    projects_in_progress.admin_order_field = 'projects_in_progress_count'

    def tasks_in_progress(self, obj):
        return obj.tasks_in_progress_count
    tasks_in_progress.admin_order_field = 'tasks_in_progress_count'

    # def calculate_total_credits(self, obj):
    #     total_credits = 0
    #     for task in obj.assigned_tasks.all():
    #         personal_grade = task.personal_grade or 0
    #         deadline_compliance = task.deadline_compliance or 0
    #         task_credits = task.task_credits or 0

    #         total_credits += (
    #             personal_grade *
    #             deadline_compliance *
    #             task_credits
    #         )
    #     return round(total_credits, 1)

    # calculate_total_credits.short_description = 'Кредиты всего'

    # def calculate_total_rating(self, obj):
    #     total_rating = 0
    #     for task in obj.assigned_tasks.all():
    #         personal_grade = task.personal_grade or 0
    #         deadline_compliance = task.deadline_compliance or 0
    #         task_credits = task.task_credits or 0
    #         intricacy_coefficient = task.intricacy_coefficient or 0
    #         manager_recommendation = task.manager_recommendation or 0
    #         total_rating += (
    #             personal_grade *
    #             deadline_compliance *
    #             task_credits *
    #             intricacy_coefficient *
    #             manager_recommendation
    #         )
    #     return round(total_rating, 1)

    # calculate_total_rating.short_description = 'Рейтинг общий'

    def calculate_total_credits(self, obj):
        total_credits = 0
        answers = AnswersStudent.objects.filter(task__assigned_student=obj)
        for answer in answers:
            personal_grade = answer.personal_grade or 0
            deadline_compliance = answer.deadline_compliance or 0
            task_credits = answer.task_credits or 0

            total_credits += (
                personal_grade
                * deadline_compliance
                * task_credits
            )
        return round(total_credits, 1)

    calculate_total_credits.short_description = 'Кредиты всего'

    def calculate_total_rating(self, obj):
        total_rating = 0
        answers = AnswersStudent.objects.filter(task__assigned_student=obj)
        for answer in answers:
            personal_grade = answer.personal_grade or 0
            deadline_compliance = answer.deadline_compliance or 0
            task_credits = answer.task_credits or 0
            intricacy_coefficient = answer.intricacy_coefficient or 0
            manager_recommendation = answer.manager_recommendation or 0
            total_rating += (
                personal_grade
                * deadline_compliance
                * task_credits
                * intricacy_coefficient
                * manager_recommendation
            )
        return round(total_rating, 1)

    calculate_total_rating.short_description = 'Рейтинг общий'

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields + ('position',)
    #     return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # при создании объекта
        if not change:
            # убедиться что значение position не None
            obj.position = obj.position or 0
        super().save_model(request, obj, form, change)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (
            None, {
                'fields': (
                    'username', 'email', 'password'
                )
            }
        ),
        (
            'Доп информация', {
                'fields': (
                    'position', 'full_name',
                    'hours_per_week', 'is_busy', 'groups'
                )
            }
        ),
        (
            'Допуски', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser'
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None, {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'username', 'email', 'position', 'full_name',
                    'password1', 'password2', 'is_active',
                    'is_staff', 'is_superuser'
                )
            }
        ),
    )
    list_display = (
        'username', 'full_name', 'is_busy',
        'position', 'projects_in_progress'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'groups'
    )
    # inlines = [ ]


@admin.register(StudentCV)
class StudentCVAdmin(admin.ModelAdmin):
    form = StudentCVForm


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    form = UniversityForm


@admin.register(BeforeUniversity)
class BeforeUniversityAdmin(admin.ModelAdmin):
    form = BeforeUniversityForm


@admin.register(StudentPortfolio)
class StudentPortfolioAdmin(admin.ModelAdmin):
    form = StudentPortfolioForm


@admin.register(UserInterestsFirst)
class UserInterestsFirstAdmin(admin.ModelAdmin):
    form = UserInterestsFirstForm


@admin.register(UserInterestsSecond)
class UserInterestsSecondAdmin(admin.ModelAdmin):
    form = UserInterestsSecondForm


@admin.register(UserInterestsThird)
class UserInterestsThirdAdmin(admin.ModelAdmin):
    form = UserInterestsThirdForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    form = ChapterForm


@admin.register(UnderSection)
class UnderSectionAdmin(admin.ModelAdmin):
    form = UnderSectionForm


@admin.register(DataKnowledge)
class DataKnowledgeAdmin(admin.ModelAdmin):
    # form = DataKnowledgeForm
    # list_display = ['chapter']

    def has_add_permission(self, request):
        return False


@admin.register(DataKnowledgeFree)
class DataKnowledgeFreeAdmin(admin.ModelAdmin):
    # form = DataKnowledgeFreeForm
    # list_display = ['chapter']

    def has_add_permission(self, request):
        return False


@admin.register(DataKnowledgeGeneral)
class DataKnowledgeGeneralAdmin(admin.ModelAdmin):
    form = DataKnowledgeGeneralForm
    actions = ['make_free', 'make_paid', 'make_both']

    def make_free(self, request, queryset):
        for obj in queryset:
            dk_free, created = DataKnowledgeFree.objects.get_or_create(
                chapter=obj.chapter,
                under_section=obj.under_section,
                defaults={
                    'video_url': obj.video_url,
                    'url': obj.url,
                }
            )
            if created:
                # Связываем файлы из DataKnowledgeGeneral с DataKnowledgeFree
                dk_free.files.set(obj.files.all())
                dk_free.save()
        self.message_user(request, "Добавлено в Базы знаний бесплатные.")

    make_free.short_description = "Назначить выбранные Базы бесплатными"

    def make_paid(self, request, queryset):
        for obj in queryset:
            dk_paid, created = DataKnowledge.objects.get_or_create(
                chapter=obj.chapter,
                under_section=obj.under_section,
                defaults={
                    'video_url': obj.video_url,
                    'url': obj.url,
                }
            )
            if created:
                # Связываем файлы из DataKnowledgeGeneral с DataKnowledge
                dk_paid.files.set(obj.files.all())
                dk_paid.save()
        self.message_user(request, "Добавлено в Базы знаний платные.")

    make_paid.short_description = "Назначить выбранные Базы платными"

    def make_both(self, request, queryset):
        for obj in queryset:
            dk_free, created_free = DataKnowledgeFree.objects.get_or_create(
                chapter=obj.chapter,
                under_section=obj.under_section,
                defaults={
                    'video_url': obj.video_url,
                    'url': obj.url,
                }
            )
            if created_free:
                dk_free.files.set(obj.files.all())
                dk_free.save()

            dk_paid, created_paid = DataKnowledge.objects.get_or_create(
                chapter=obj.chapter,
                under_section=obj.under_section,
                defaults={
                    'video_url': obj.video_url,
                    'url': obj.url,
                }
            )
            if created_paid:
                dk_paid.files.set(obj.files.all())
                dk_paid.save()

        self.message_user(
            request,
            "Добалено в бесплатные и платные Базы знаний."
        )

    make_both.short_description = "Добавить в бесплатные и платные Базы знаний"


class ProjectInline(TabularInline):
    model = Project.group.through
    extra = 1
    verbose_name = _('Проект')
    verbose_name_plural = _('Проекты')


@admin.register(GroupStudent)
class GroupAdmin(admin.ModelAdmin):
    form = GroupStudentForm
    list_display = ('name', 'get_students_table')
    list_filter = (
        # Используем связанные поля из модели Student
        'students__university', 'students__course')

    # def get_students_table(self, obj):
    #     # Создаем таблицу с данными о студентах
    #     table_html = "<table>"
    #     table_html += (
    #         "<tr><th>ФИО</th><th>Мобильный телефон</th>"
    #         "<th>Электронная почта</th>"
    #         "<th>Ник в Телеграм</th><th>Возраст</th>"
    #         "<th>Пол</th><th>ВУЗ</th><th>Курс</th>"
    #         "<th>Факультет</th><th>Статус</th><th>Часов в неделю</th></tr>"
    #     )
    #     for student in obj.students.all():
    #         edit_url = reverse(
    #             'admin:%s_%s_change'
    #             % (student._meta.app_label, student._meta.model_name),
    #             args=[student.pk]
    #         )
    #         table_html += (
    #             f"<tr><td><a href='{edit_url}'>{student.full_name}</a></td>"
    #             f"<td>{student.mobile_phone}</td>"
    #             f"<td>{student.email}</td><td>{student.tg_nickname}</td><td>{student.age}</td><td>{student.gender}</td>"
    #             f"<td>{student.university}</td><td>{student.course}</td><td>{student.faculty}</td><td></td>"
    #             f"<td>{student.hours_per_week}</td></tr>"
    #         )

    #     table_html += "</table>"
    #     return format_html(table_html)

    def get_students_table(self, obj):
        students = obj.students.all()
        students_list = []
        for student in students:
            edit_url = reverse(
                'admin:%s_%s_change'
                % (student._meta.app_label, student._meta.model_name),
                args=[student.pk]
            )
            students_list.append(
                {
                    'full_name': student.full_name,
                    'mobile_phone': student.mobile_phone,
                    'email': student.email,
                    'tg_nickname': student.tg_nickname,
                    'age': student.age,
                    'gender': student.gender,
                    'university': student.university,
                    'course': student.course,
                    'faculty': student.faculty,
                    'hours_per_week': student.hours_per_week,
                    'change_url': edit_url,
                }
            )
        # контекст для шаблона
        context = {
            'students': students_list
        }
        # Рендер шаблона с данными
        table_html = render_to_string('students_table.html', context)
        return format_html(table_html)

    get_students_table.short_description = 'Специалисты'
    inlines = [ProjectInline]


class CommentInline(TabularInline):
    model = Comment
    extra = 1
    form = CommentForm
    fk_name = 'project'


class TaskGroupInline(TabularInline):
    model = TaskGroup
    form = TaskGroupForm
    fk_name = 'project'


# @admin.register(TaskStudent)
class TaskStudentInline(TabularInline):
    model = TaskStudent
    form = TaskStudentForm
    fk_name = 'project'
    # extra = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # result = queryset.filter(
        #     student__full_name='student'
        # ).order_by('start_date')
        result = queryset.order_by(
            'assigned_student__full_name',
            '-start_date'
        )
        return result

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(
            TaskStudentInline, self
        ).get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['assigned_student'].queryset = (
                Student.objects.filter(projects=obj)
            )
        formset.extra = 1
        return formset

    # # получить id для вывода студентов назначенных на проект
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "assigned_student":
    #         # Получаем id проекта из запроса, если он есть
    #         project_id = request.resolver_match.kwargs['object_id']
    #         project = Project.objects.get(pk=project_id)
    #         kwargs["queryset"] = project.students.all()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ['name', 'get_students', 'captain', 'is_completed']
    inlines = [
        CommentInline, TaskStudentInline,
        TaskGroupInline,
    ]

    def get_students(self, obj):
        return ", ".join([str(student) for student in obj.students.all()])
    get_students.short_description = 'Специалисты'


class TaskStatusStudentInline(TabularInline):
    model = TaskStatusStudent
    form = TaskStatusStudentForm
    extra = 1
    fk_name = 'task_student'


class AnswersStudentInline(TabularInline):
    model = AnswersStudent
    form = AnswersStudentForm
    extra = 1


@admin.register(TaskStudent)
class TaskStudentAdmin(admin.ModelAdmin):
    # ... other configurations ..
    form = TaskStudentForm
    # ordering = ['student', '-start_date']
    ordering = ['assigned_student', '-created_at']
    # Add the TaskStatusStudentInline to the inlines list
    inlines = [TaskStatusStudentInline, AnswersStudentInline]
    list_display = [
        'project', 'description', 'assigned_student',
        'project_cost', 'end_date', 'status',
        'total_credits', 'total_rating'
    ]

    # настраивает список студентов для уже существующих объектов
    def get_form(self, request, obj=None, **kwargs):
        # Это предполагает, что project_id может быть передан как GET параметр
        project_id = request.GET.get('project_id')
        if project_id:
            kwargs['initial'] = {'project': project_id}
        form = super(TaskStudentAdmin, self).get_form(request, obj, **kwargs)
        return form

    # для случая, когда форма первоначально рендерится с ID проекта
    # (например, при добавлении новой задачи со страницы деталей проекта)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'assigned_student' and 'project' in request.GET:
            project_id = request.GET['project']
            kwargs['queryset'] = Student.objects.filter(
                projects__id=project_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Аннотация запросов для добавления вычисленных полей
        return TaskStudent.annotated_aggregates(queryset)

    # def calculate_total_task_credits(self, obj):
    #     personal_grade = obj.personal_grade or 0
    #     deadline_compliance = obj.deadline_compliance or 0
    #     task_credits = obj.task_credits or 0
    #     return round(
    #         personal_grade *
    #         deadline_compliance *
    #         task_credits,
    #         1
    #     )
    def total_credits(self, obj):
        return obj.total_credits

    total_credits.short_description = 'Кредиты по задаче'

    # def calculate_rating(self, obj):
    #     total_task_credits = self.calculate_total_task_credits(obj) or 0
    #     intricacy_coefficient = obj.intricacy_coefficient or 0
    #     manager_recommendation = obj.manager_recommendation or 0
    #     return round(
    #         total_task_credits *
    #         intricacy_coefficient *
    #         manager_recommendation,
    #         1
    #     )
    def total_rating(self, obj):
        return obj.total_rating

    total_rating.short_description = 'Рейтинг по задаче'


class TaskGroupStudentInline(TabularInline):
    model = TaskStatusGroup
    extra = 1
    form = TaskStatusGroupForm
    fk_name = 'task_group'


class AnswerGroupInline(TabularInline):
    model = AnswerGroup
    extra = 1
    form = AnswerGroupForm
    fk_name = 'answer'


@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    # ... other configurations ...
    form = TaskGroupForm
    # Add the TaskStatusStudentInline to the inlines list
    inlines = [TaskGroupStudentInline, AnswerGroupInline]


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    form = MailingTranslationForm


class AnswerAnswerGroupInline(TabularInline):
    model = AnswerTestTask
    extra = 1
    form = AnswerTestTaskForm
    fk_name = 'answer'


class TestTaskEvaluationInline(TabularInline):
    model = TestTaskEvaluation
    extra = 0
    # form = TestTaskEvaluationForm
    fk_name = 'assigned_testtask'


@admin.register(TestTask)
class TestTaskAdmin(admin.ModelAdmin):
    # ... other configurations ...
    form = TestTaskForm
    list_display = (
        'title', 'description', 'task_duration'

    )
    # Add the TaskStatusStudentInline to the inlines list
    # inlines = [AnswerAnswerGroupInline]
    inlines = [TestTaskEvaluationInline]


@admin.register(TestTaskEvaluation)
class TestTaskEvaluationAdmin(admin.ModelAdmin):
    form = TestTaskEvaluationForm
    list_display = (
        'student', 'url', 'score', 'comment',
        'assigned_testtask', 'is_completed', 'telegram_user_id'
    )
    list_editable = ['score', 'is_completed', 'comment']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    form = OrdersForm


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm
    list_display = (
        'user', 'duration', 'expiration_timestamp', 'is_active'
    )


class StudentInvitationInline(admin.TabularInline):
    model = StudentInvitation
    form = StudentInvitationForm
    extra = 1


@admin.register(ProjectInvitation)
class ProjectInvitationAdmin(admin.ModelAdmin):
    form = ProjectInvitationForm
    list_display = (
        'project', 'invitation_duration',
        'created_at', 'updated_at', 'is_expired'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('project__name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StudentInvitationInline]

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.short_description = 'Приглашение закрыто'
    is_expired.boolean = True


@admin.register(StudentInvitation)
class StudentInvitationAdmin(admin.ModelAdmin):
    form = StudentInvitationForm
    list_display = ('invitation', 'student', 'reaction_status')
    list_filter = ('reaction_status',)
    search_fields = ('student__full_name', 'invitation__project__name')
