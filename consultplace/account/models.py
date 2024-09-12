import os

# from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, SET_NULL, Avg, BigIntegerField,
                              BooleanField, CharField, Count, DateField,
                              DateTimeField, DecimalField, EmailField,
                              ExpressionWrapper, F, FileField, FloatField,
                              ForeignKey, ImageField, IntegerField,
                              ManyToManyField, Max, Model, OneToOneField,
                              PositiveIntegerField, PositiveSmallIntegerField,
                              Q, Sum, TextField, URLField)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

from .calculations import calculate_rating

CURRENT_STATUSES = [
    (_('В работе'), _('Busy')),
    (_('Свободен'), _('Free')),
]

USER_POSITIONS = [
    (_('Тимлид'), _('Teamlead')),
    (_('Трекер'), _('Tracker')),
    (_('Админ'), _('Admin')),
]
# SPECIALIST_POSITIONS = [
#     (_('Не определен'), _('Default')),
#     (_('Студент'), _('Student')),
#     (_('Стажер'), _('Trainee')),
#     (_('Аналитик'), _('Analyst')),
# ]
SPECIALIST_POSITIONS = [
    (0, 'Not specified'),
    (1, 'Student'),
    (2, 'Trainee'),
    (3, 'Analyst')
]
BOOLEAN_CHOICES = [
    (_('Да'), _('Yes')),
    (_('Нет'), _('No')),
]
SCORE_CHOICES = [
    (0, 'В работе'),
    (1, 'Предложить обучение'),
    (2, 'Предложить стажировку'),
    (3, 'Штат аналитиков')
]
DURATION_CHOICES = [
    (1, '1 месяц'),
    (3, '3 месяца'),
    (6, '6 месяцев'),
    (12, '12 месяцев'),
]
# CHECKUP_STATUSES = [
#     (_('Не определено'), _('Not specified')),
#     (_('Предложить правки'), _('Suggest edits')),
#     (_('Отправить фидбэк'), _('Submit feedback')),
# ]

CHECKUP_STATUSES = [
    (0, 'Not specified'),
    (1, 'Suggest edits'),
    (2, 'Submit feedback'),
]


class CustomUser(AbstractUser):
    is_busy = CharField(
        max_length=50,
        choices=CURRENT_STATUSES,
        verbose_name=_('Текущий статус'),
        default='Free'
    )
    position = CharField(
        max_length=50,
        choices=USER_POSITIONS,
        verbose_name=_('Должность'),
        default='Teamlead'
    )
    full_name = CharField(
        max_length=255,
        verbose_name=_('ФИО')
    )
    hours_per_week = PositiveIntegerField(
        verbose_name=_('Сколько часов готовы уделять в неделю'),
        default=0
    )

    # def projects_in_progress(self):
    #     return self.captain.annotate(
    #         in_progress_count=Count(
    #             'tasks',
    #             filter=Q(tasks__status__in=[
    #                 'in_progress', 'being_performed', 'awaiting_os',
    #                 'under_revision', 'on_pause'
    #             ])
    #         )
    #     ).values_list('in_progress_count', flat=True).count() or 0

    def projects_in_progress(self):
        # Получаем queryset проектов, где пользователь является капитаном
        projects = Project.objects.filter(captain=self)

        # Считаем количество проектов,
        # у которых хотя бы одна задача не выполнена
        projects_in_progress = projects.filter(
            tasks__status__in=[
                'in_progress', 'being_performed', 'awaiting_os',
                'under_revision', 'on_pause'
            ]
        ).distinct().count()

        return projects_in_progress

    projects_in_progress.short_description = 'Проектов в работе'


class UserInterestsFirst(Model):
    interest = CharField(
        verbose_name=_('Интерес'),
        max_length=150
    )

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = _('Профессиональная сфера интересов')
        verbose_name_plural = _('Профессиональная сфера интересов')


class UserInterestsSecond(Model):
    interest = CharField(
        verbose_name=_('Интерес'),
        max_length=150
    )

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = _('Интересующие Вас ниши')
        verbose_name_plural = _('Интересующие Вас ниши')


class UserInterestsThird(Model):
    interest = CharField(
        verbose_name=_('Интерес'),
        max_length=150
    )

    def __str__(self):
        return self.interest

    class Meta:
        verbose_name = _('Цели')
        verbose_name_plural = _('Цели')


class BeforeUniversity(Model):
    name = CharField(
        max_length=125,
        verbose_name=_('Наименования')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Образование')
        verbose_name_plural = _('Образование')


class University(Model):
    name = CharField(
        max_length=125,
        verbose_name=_('Наименования')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ВУЗ')
        verbose_name_plural = _('ВУЗ')


class Course(Model):
    name = CharField(
        max_length=125,
        verbose_name=_('Наименования')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курс')


MANAGER_STATUSES = [
    (_('Manager Lead'), _('Лид менеджера')),
    (_('In Progress with Manager'), _('В работе у менеджера')),
    (_('Rejected'), _('Отказ')),
    (_('Awaiting Payment'), _('Ожидает оплаты')),
    (_('Partially Paid'), _('Частично оплачен')),
    (_('Paid'), _('Оплачен')),
]

EDUCATION_STATUSES = [
    (_('Base'), _('Базовый')),
    (_('Optimal'), _('Оптимальный')),
    (_('Advanced'), _('Продвинутый')),
    (_('Free participation'), _('Басплатное участие')),
    (_('Dropout'), _('Выбыл')),
    (_('Grant'), _('Грант')),
]


class Student(Model):
    # Обязательные поля
    full_name = CharField(
        max_length=255,
        verbose_name=_('ФИО')
    )
    mobile_phone = CharField(
        max_length=25,
        verbose_name=_('Мобильный телефон')
    )
    email = EmailField(
        verbose_name=_('Электронная почта')
    )
    tg_nickname = CharField(
        max_length=50,
        verbose_name=_('Ник в Телеграм'),
        unique=True
    )
    age = PositiveIntegerField(
        verbose_name=_('Возраст')
    )
    gender = CharField(
        max_length=50,
        verbose_name=_('Пол')
    )
    before_university = ForeignKey(
        BeforeUniversity,
        verbose_name=_('Образование'),
        on_delete=CASCADE
    )
    university = ForeignKey(
        University,
        verbose_name=_('ВУЗ'),
        on_delete=CASCADE
    )
    faculty = CharField(
        max_length=255,
        verbose_name=_('Факультет')
    )
    course = ForeignKey(
        Course,
        verbose_name=_('Курс'),
        on_delete=CASCADE
    )
    interest_first = ManyToManyField(
        'UserInterestsFirst',
        verbose_name=_('Профессиональная сфера интересов'),
        blank=True
    )
    other_interest_first = CharField(
        max_length=150,
        verbose_name=_('Профессиональная сфера интересов другое'),
        null=True,
        blank=True
    )
    interest_second = ManyToManyField(
        'UserInterestsSecond',
        verbose_name=_('Интересующие Вас ниши'),
        blank=True
    )
    other_interest_second = CharField(
        max_length=150,
        verbose_name=_('Интересующие Вас ниши другое'),
        null=True,
        blank=True
    )
    interest_third = ManyToManyField(
        'UserInterestsThird',
        verbose_name=_('Цели'),
        blank=True
    )
    other_interest_third = CharField(
        max_length=150,
        verbose_name=_('цели другие'),
        null=True,
        blank=True
    )
    manager_status = CharField(
        max_length=50,
        choices=MANAGER_STATUSES,
        verbose_name=_('Статус менеджера')
    )
    education_status = CharField(
        max_length=50,
        choices=EDUCATION_STATUSES,
        verbose_name=_('Статус обучения')
    )

    hours_per_week = PositiveIntegerField(
        verbose_name=_('Сколько часов готовы уделять в неделю')
    )
    telegram_user_id = BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='Телеграм ID User'
    )
    subscription_end_date = DateField(
        verbose_name='Дата окончания подписки',
        blank=True,
        null=True
    )
    date_joined = DateTimeField(
        _("date joined"),
        default=timezone.now
    )
    is_busy = CharField(
        max_length=50,
        choices=CURRENT_STATUSES,
        verbose_name=_('Текущий статус'),
        default='Free'
    )
    position = IntegerField(
        choices=SPECIALIST_POSITIONS,
        verbose_name=_('Должность'),
        default=0
    )
    # test_grade = models.IntegerField(
    #     verbose_name=_('Тестовая оценка'),
    #     null=True,
    #     blank=True,
    #     default=0
    # )
    # subscription = models.OneToOneField(
    #     'Subscription',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='student'
    # )

    def __str__(self):
        return self.full_name

    def get_last_mailing(self):
        last_mailing = self.mailings.aggregate(
            last_sent=Max('sent_date')
        )['last_sent']
        if last_mailing:
            return self.mailings.get(sent_date=last_mailing)
        return None

    def projects_in_group(self):
        project_count = (
            Project.objects.
            filter(group__students=self)
            .annotate(num_projects=Count('id'))
            .aggregate(total=Sum('num_projects'))
        )['total']
        return project_count

    def projects_in_progress(self):
        """
        Подсчитать поличество проектов в работе.
        """
        projects = self.projects.annotate(
            num_incomplete_tasks=Count(
                'tasks', filter=~Q(tasks__status='finished')
            )).count()
        return projects

    projects_in_progress.short_description = 'Проектов в работе'

    def tasks_in_progress(self):
        """
        Подсчитать количество задач,
        которые в данный момент находятся в работе.
        """
        return self.assigned_tasks.filter(~Q(status='finished')).count()

    tasks_in_progress.short_description = 'Задач в работе'

    @classmethod
    def annotate_with_aggregates(cls, queryset):
        """
        Аннотирует queryset студентов количеством проектов и задач в работе.
        """
        return queryset.annotate(
            projects_in_progress_count=Count(
                'projects',
                filter=~Q(projects__tasks__status='finished'),
                distinct=True
            ),
            tasks_in_progress_count=Count(
                'assigned_tasks',
                filter=~Q(assigned_tasks__status='finished')
            )
        )

    def calculate_aggregate_values(self):
        total_credits = self.answersstudent_set.aggregate(
            totla_credits=Sum('total_credits')
        )['total_credits'] or 0
        total_rating = self.answersstudent_set.aggregate(
            total_rating=Sum('total_rating')
        )['total_rating'] or 0
        return round(total_credits, 1), round(total_rating, 1)
    # def subscription_status(self):
    #     if self.subscription:
    #         if self.subscription.is_active():
    #             return 'активна'
    #         else:
    #             expiration_date = datetime.fromtimestamp(
    #                 self.subscription.expiration_timestamp
    #             )
    #             return f'окончена ({expiration_date.strftime("%d.%m.%Y")})'
    #     return 'нет подписки'

    # subscription_status.short_description = 'Подписка'
    class Meta:
        verbose_name = _('Специалист')
        verbose_name_plural = _('Специалисты')


class Subscription (Model):
    user = OneToOneField(
        Student,
        on_delete=CASCADE,
        # related_name='student_subscription',
        verbose_name='Пользователь'
    )
    duration = PositiveSmallIntegerField(
        choices=DURATION_CHOICES,
        verbose_name='Срок подписки (мес)'
    )
    expiration_timestamp = BigIntegerField(
        verbose_name='Время окончания подписки (таймстамп)',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.full_name} - {self.get_duration_display()}'

    def save(self, *args, **kwargs):
        import time
        current_time = int(time.time())
        self.expiration_timestamp = (
            current_time + self.duration * 30 * 24 * 60 * 60
        )
        super(Subscription, self). save(*args, **kwargs)

    def is_active(self):
        import time
        current_time = int(time.time())
        if current_time < self.expiration_timestamp:
            return True
        return False

    is_active.boolean = False
    is_active.short_description = 'Статус подписки'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class StudentCV(Model):
    student = ForeignKey(
        Student,
        verbose_name=_('Специалист'),
        on_delete=CASCADE
    )
    file = FileField(
        verbose_name=_('Резюме специалиста'),
        upload_to='student_cv'
    )
    create_date = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    def __str__(self):
        if self.student:
            return self.student.full_name
        else:
            return "StudentCV without associated student"

    class Meta:
        verbose_name = _('Резюме специалиста')
        verbose_name_plural = _('Резюме специалистов')


class StudentPortfolio(Model):
    student = ForeignKey(
        Student,
        verbose_name=_('Специалист'),
        on_delete=CASCADE
    )
    file = FileField(
        verbose_name=_('Портфолио специалиста'),
        upload_to='student_cv'
    )
    create_date = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    def __str__(self):
        if self.student:
            return self.student.full_name
        else:
            return "StudentCV without associated student"

    class Meta:
        verbose_name = _('Портфолио специалиста')

        verbose_name_plural = _('Портфолио специалиста')


class GroupStudent(Model):
    name = CharField(
        max_length=100,
        verbose_name=_('Название группы')
    )
    captain = ForeignKey(
        Student,
        on_delete=CASCADE,
        null=True,
        related_name='captain_group_students'
    )
    students = ManyToManyField(
        Student,
        related_name='group_students'
    )
    create_date = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(GroupStudent, self).save(*args, **kwargs)
        group_projects = self.project_set.all()
        for student in self.students.all():
            student.projects.add(*group_projects)

    class Meta:
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')


# def calculate_rating(
#     self, personal_grade, deadline_compliance,
#     manager_recommendation, group_grade, intricacy_coefficient
# ):
#     if (
#         personal_grade is not None and
#         deadline_compliance is not None and
#         manager_recommendation is not None and
#         group_grade is not None and
#         intricacy_coefficient is not None
#     ):
#         rating = round(
#             (
#                 0.3 * personal_grade +
#                 0.2 * deadline_compliance +
#                 0.2 * manager_recommendation +
#                 0.3 * group_grade
#             ) * intricacy_coefficient, 1
#         )
#         return rating

class Project(Model):
    group = ManyToManyField(
        GroupStudent,
        verbose_name=_('Группа')
    )
    students = ManyToManyField(
        Student,
        verbose_name=_('Специалист'),
        through='Student_projects',
        related_name='projects'
    )
    captain = ForeignKey(
        CustomUser,
        verbose_name=_('Капитан'),
        related_name='captain',
        on_delete=CASCADE,
        null=True
    )
    name = CharField(
        max_length=300,
        verbose_name=_('Наименование')
    )
    intricacy = CharField(
        max_length=250,
        verbose_name=_('Сложность')
    )
    start_date = DateField(
        verbose_name=_('Дата начала'),
        null=True,
        blank=True
    )
    end_date = DateField(
        verbose_name=_('Дата окончания'),
        null=True,
        blank=True
    )
    group_grade = FloatField(
        max_length=10,
        verbose_name=_('Групповая оценка'),
        blank=True,
        null=True
    )
    intricacy_coefficient = FloatField(
        max_length=10,
        verbose_name='Коэффициент сложности',
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1.5)]
    )
    pinned_dataknowledge = ManyToManyField(
        'DataKnowledgeGeneral',
        verbose_name=_('Методология'),
        through='ProjectDataKnowledge',
        related_name='pinned_dataknowledge'
    )

    def __str__(self):
        return self.name

    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def calculate_task_rating(self):

        personal_grade_avg = (
            self.tasks.filter(personal_grade__isnull=False)
            .aggregate(Avg('personal_grade'))['personal_grade__avg']
        )
        deadline_compliance_avg = (
            self.tasks.filter(deadline_compliance__isnull=False)
            .aggregate(
                Avg('deadline_compliance')
            )['deadline_compliance__avg']
        )
        manager_recommendation_avg = (
            self.tasks.filter(manager_recommendation__isnull=False)
            .aggregate(
                Avg('manager_recommendation')
            )['manager_recommendation__avg']
        )

        rating = calculate_rating(
            personal_grade_avg,
            deadline_compliance_avg,
            manager_recommendation_avg,
            self.group_grade,
            self.intricacy_coefficient
        )
        return rating

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        task_rating = self.calculate_task_rating()
        for task in self.tasks.all():
            task.task_rating = task_rating
            task.save()

    def is_completed(self):
        return 'Завершен' if all(
            task.status == 'finished' for task in self.tasks.all()
        ) else 'Не завершен'

    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекты')


class ProjectDataKnowledge(Model):
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name='project_dataknowledge_set'
    )
    dataknowledge = ForeignKey(
        "DataKnowledgeGeneral",
        on_delete=CASCADE,
        related_name='pinned_dataknowledges_set'
    )

    class Meta:
        unique_together = ('project', 'dataknowledge')


class Student_projects(Model):
    student = ForeignKey(
        Student,
        on_delete=SET_NULL,
        null=True,
        related_name='project_student'
    )
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name='student_projects_set'
    )
    # group_student = models.ForeignKey(
    #     GroupStudent,
    #     on_delete=models.CASCADE
    # )

    class Meta:
        unique_together = ('student', 'project')


class Comment(Model):
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name=_('Проект')
    )
    user = ForeignKey(
        CustomUser,
        verbose_name=_('админ'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    student = ForeignKey(
        Student,
        verbose_name=_('Капитан группы'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    comment_text = TextField(
        verbose_name=_('Текст комментария')
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    def __str__(self):
        return str(self.project)

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')


class TestTask(Model):
    title = CharField(
        max_length=255,
        verbose_name='Название задания',
        blank=True,
        null=True
    )
    description = TextField(
        verbose_name=_('Описание')
    )
    url = URLField(
        verbose_name=_('Ссылка на задание'),
        null=True,
        blank=True
    )
    task_duration = IntegerField(
        verbose_name=_('Срок выполнения (дни)'),
        null=True,
        blank=True,
        default=3
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Задача тестовое')
        verbose_name_plural = _('Задачи тестовые')


class TestTaskEvaluation(Model):
    student = OneToOneField(
        Student,
        verbose_name=_('Специалист'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    telegram_user_id = IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='Телеграм ID User'
    )
    is_completed = CharField(
        choices=BOOLEAN_CHOICES,
        max_length=50,
        default=_('Нет'),
        verbose_name='Статус'
    )
    url = URLField(
        verbose_name=_('Выполненное задание (ссылка)'),
        null=True,
        blank=True
    )
    score = IntegerField(
        choices=SCORE_CHOICES,
        verbose_name=_('Оценка'),
        default=0
    )
    comment = TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('Сообщение')
    )
    assigned_testtask = ForeignKey(
        TestTask,
        verbose_name=_('Предложенная задача'),
        on_delete=CASCADE
    )
    date_accepted = DateTimeField(
        verbose_name=_('Дата получения'),
        default=timezone.now,
        blank=True
    )

    class Meta:
        verbose_name = _('Оценка тестового')
        verbose_name_plural = _('Оценки тестовых')

    # def save_position(self, *args, **kwargs):
    #     super(). save(**args, **kwargs)
    #     if self.score == 1:
    #         self.student.position = 'Student'
    #     elif self.score == 2:
    #         self.student.position = 'Trainee'
    #     elif self.score == 3:
    #         self.student.position = 'Analyst'
    #     self.student.save()

    def save(self, *args, **kwargs):
        if self.telegram_user_id and not self.student:
            try:
                student = Student.objects.get(
                    telegram_user_id=self.telegram_user_id
                )
                self.student = student
            except Student.DoesNotExist:
                raise ValueError(
                    'Специалиста с таким телеграм айди не существует'
                )
        super().save(*args, **kwargs)
        self.update_student_position()

    def update_student_position(self):
        """Обновить позицию студента на основе оценки."""
        if self.score == 1:
            new_position = 1
        elif self.score == 2:
            new_position = 2
        elif self.score == 3:
            new_position = 3
        else:
            new_position = 0

        # Обновление позиции студента без дополнительной перезагрузки объекта
        Student.objects.filter(
            id=self.student.id).update(
            position=new_position
        )

    def update_score(self, new_score):
        """Метод для обновления только оценки и комментария."""
        self.score = new_score
        self.save(update_fields=['score'])

    def __str__(self):
        return f"{self.student} - {self.assigned_testtask}"


class AnswerTestTask(Model):
    file = FileField(
        verbose_name=_('Ответ файлом'),
        upload_to='file_a',
        null=True,
        blank=True
    )
    url = URLField(
        verbose_name=_('Ответ ссылкой'),
        null=True,
        blank=True
    )
    answer = ForeignKey(
        TestTask,
        verbose_name=_('Ответ по задаче'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    user = ForeignKey(
        CustomUser,
        verbose_name=_('Пользователь'),
        on_delete=CASCADE
    )

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = _('Ответы')
        verbose_name_plural = _('Ответы')


class TaskGroup(Model):
    project = ForeignKey(
        Project,
        verbose_name=_('Проект'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    description = TextField(
        verbose_name=_('Описание')
    )
    project_cost = CharField(
        max_length=120,
        verbose_name=_("Стоимость"),
        null=True,
        blank=True
    )
    start_date = DateField(
        verbose_name=_('Дата начала'),
        null=True,
        blank=True
    )
    end_date = DateField(
        verbose_name=_('Дата окончания'),
        null=True,
        blank=True
    )
    grade = IntegerField(
        verbose_name=_('оценка'),
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.description)

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        verbose_name = _('Задача группы по проекту')
        verbose_name_plural = _('Задача группы по проекту')


STATUS_CHOICES = [
    ('in_progress', _('В работу')),
    ('being_performed', _('Выполняется')),
    ('completed', _('Выполнена')),
    ('awaiting_os', _('Ожидает ОС')),
    ('under_revision', _('На правках')),
    ('finished', _('Завершена')),
    ('on_pause', _('На паузе')),
]


class AnswerGroup(Model):
    file = FileField(
        verbose_name=_('Ответ файлом'),
        upload_to='file_a',
        null=True,
        blank=True
    )
    url = URLField(
        verbose_name=_('Ответ ссылкой'),
        null=True,
        blank=True
    )
    answer = ForeignKey(
        TaskGroup,
        verbose_name=_('Ответ группы'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    user = ForeignKey(
        'CustomUser',
        verbose_name=_('Пользователь'),
        on_delete=CASCADE
    )

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = _('Ответ группы')
        verbose_name_plural = _('Ответ группы')


# закоментить
class TaskStatusGroup(Model):
    task_group = ForeignKey(
        TaskGroup,
        verbose_name=_('Задача группы'),
        on_delete=CASCADE
    )
    date_create = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    status = CharField(
        max_length=50,
        verbose_name=_('Статус'),
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = _('Статус задачи группы')
        verbose_name_plural = _('Статус задачи группы')


class TaskStudent(Model):
    project = ForeignKey(
        Project,
        verbose_name=_('Проект'),
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    title = CharField(
        verbose_name=_('Заголовок'),
        max_length=250,
        null=True,
        blank=True
    )
    assigned_student = ForeignKey(
        Student,
        verbose_name=_('Специалист'),
        on_delete=CASCADE,
        related_name='assigned_tasks'
    )
    description = TextField(
        verbose_name=_('Описание')
    )
    pinned_dataknowledge = ManyToManyField(
        'DataKnowledgeGeneral',
        verbose_name=_('Методология'),
        through='TaskStudentDataKnowledge',
        related_name='pinned_taskdataknowledge'
    )
    notice = TextField(
        verbose_name=_('Примечание'),
        blank=True,
        null=True
    )
    material = TextField(
        verbose_name=_('Материалы'),
        blank=True,
        null=True
    )
    project_cost = CharField(
        max_length=120,
        verbose_name=_("Стоимость"),
        null=True,
        blank=True
    )
    start_date = DateField(
        verbose_name=_('Дата начала'),
        null=True,
        blank=True
    )
    end_date = DateField(
        verbose_name=_('Дата окончания'),
        null=True,
        blank=True
    )
    # need change name to project_rate & max value = 2
    personal_grade = FloatField(
        validators=[MaxValueValidator(2)],
        verbose_name=_('Оценка по проекту'),
        blank=True,
        null=True
    )
    # change to max value as 1
    deadline_compliance = FloatField(
        validators=[MaxValueValidator(1)],
        verbose_name=_('Соблюдение дедлайнов'),
        blank=True,
        null=True
    )
    manager_recommendation = FloatField(
        validators=[MaxValueValidator(2)],
        verbose_name=_('Рекомендация менеджера'),
        blank=True,
        null=True
    )
    intricacy_coefficient = FloatField(
        verbose_name=_('Коэффициент сложности'),
        validators=[MaxValueValidator(2)],
        blank=True,
        null=True
    )
    task_credits = FloatField(
        verbose_name=_('Кредиты'),
        validators=[MaxValueValidator(30)],
        blank=True,
        null=True
    )
    created_at = DateTimeField(
        verbose_name='Дата и время создания',
        default=timezone.now
    )
    status = CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='in_progress',
        verbose_name=_('Статус')
    )

    def __str__(self):
        return (
            f'"{self.project.name}" {self.title}'
        ) if self.title else "Без названия"

    @property
    def execution_period(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    @classmethod
    def annotated_aggregates(cls, queryset):

        return queryset.annotate(
            total_credits=Sum(
                F('answersstudent__personal_grade')
                * F('answersstudent__deadline_compliance')
                * F('answersstudent__task_credits')
            ),
            total_rating=Sum(
                F('answersstudent__personal_grade')
                * F('answersstudent__deadline_compliance')
                * F('answersstudent__task_credits')
                * F('answersstudent__intricacy_coefficient')
                * F('answersstudent__manager_recommendation')
            )
        )

    def to_dict(self):
        assigned_student = (
            self.assigned_student.full_name
            if self.assigned_student
            else None
        )
        task_dict = {
            "id": self.id,
            "project": self.project.name if self.project else None,
            "title": self.title,
            "assigned_student": assigned_student,
            "description": self.description,
            "notice": self.notice,
            "material": self.material,
            "project_cost": self.project_cost,
            "start_date": self.start_date,
            "end_date": self.end_date,
            # "personal_grade": self.personal_grade,
            # "deadline_compliance": self.deadline_compliance,
            # "manager_recommendation": self.manager_recommendation,
            # "intricacy_coefficient": self.intricacy_coefficient,
            # "task_credits": self.task_credits,
            # "created_at": self.created_at,
            # "status": self.status,
            "pinned_dataknowledge": [
                {
                    "chapter_name": (
                        dk.chapter.name if dk.chapter else "No Chapter"
                    ),
                    "under_section_name": (
                        dk.under_section.name
                        if dk.under_section else "No Section"
                    ),
                    "files": (
                        ", ".join(file.name for file in dk.files.all())
                        if dk.files else "No Files"
                    ),
                    "video_url": dk.video_url or "No Video",
                    "url": dk.url or "No URL",
                }
                for dk in self.pinned_dataknowledge.all()
            ]
        }
        return task_dict

    class Meta:
        verbose_name = _('Задача специалиста по проекту')
        verbose_name_plural = _('Задачи специалистов по проекту')


class TaskStudentDataKnowledge(Model):
    task = ForeignKey(
        TaskStudent,
        on_delete=CASCADE,
        related_name='taskstudent_dataknowledge_set'
    )
    dataknowledge = ForeignKey(
        "DataKnowledgeGeneral",
        on_delete=CASCADE,
        related_name='taskstudent_dataknowledge_set'
    )

    class Meta:
        unique_together = ('task', 'dataknowledge')


class AnswersStudent(Model):
    file = FileField(
        verbose_name='Ответ файлом',
        upload_to='file_a',
        null=True,
        blank=True
    )
    url = URLField(
        verbose_name=_('Ответ ссылкой'),
        null=True,
        blank=True
    )
    comment = TextField(
        verbose_name=_('Комментарий'),
        blank=True,
        null=True
    )
    status = IntegerField(
        # max_length=50,
        choices=CHECKUP_STATUSES,
        verbose_name=_('Статус проверки'),
        default=0
    )
    task = ForeignKey(
        TaskStudent,
        verbose_name=_('Задача студента'),
        on_delete=CASCADE,
        null=True,
        blank=True
    )
    personal_grade = FloatField(
        validators=[MaxValueValidator(2)],
        verbose_name=_('Оценка по проекту'),
        blank=True,
        null=True,
        default=0
    )
    # change to max value as 1
    deadline_compliance = FloatField(
        validators=[MaxValueValidator(1)],
        verbose_name=_('Соблюдение дедлайнов'),
        blank=True,
        null=True,
        default=0
    )
    manager_recommendation = FloatField(
        validators=[MaxValueValidator(2)],
        verbose_name=_('Рекомендация менеджера'),
        blank=True,
        null=True,
        default=0
    )
    intricacy_coefficient = FloatField(
        verbose_name=_('Коэффициент сложности'),
        validators=[MaxValueValidator(2)],
        blank=True,
        null=True,
        default=0
    )
    # change field type to floatfield
    task_credits = FloatField(
        verbose_name=_('Кредиты'),
        validators=[MaxValueValidator(30)],
        blank=True,
        null=True,
        default=0
    )
    # comment this
    # user = models.ForeignKey(
    #     CustomUser,
    #     verbose_name='Пользователь',
    #     on_delete=models.CASCADE
    # )
    created_at = DateTimeField(
        verbose_name=_('Создано'),
        default=timezone.now
    )

    def __str__(self):
        return str(self.url)

    @classmethod
    def annotated_aggregates(cls, queryset):
        return queryset.annotate(
            total_credits=ExpressionWrapper(
                F('personal_grade')
                * F('deadline_compliance')
                * F('task_credits'),
                output_field=FloatField()
            ),
            total_rating=ExpressionWrapper(
                F('total_credits')
                * F('intricacy_coefficient')
                * F('manager_recommendation'),
                output_field=FloatField()
            )
        )

    class Meta:
        verbose_name = _('Ответ специалиста')
        verbose_name_plural = _('Ответы специалистов')


# закоментить
class TaskStatusStudent(Model):
    task_student = ForeignKey(
        TaskStudent,
        verbose_name=_('Задача студента'),
        on_delete=CASCADE
    )
    date_create = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    status = CharField(
        max_length=50,
        verbose_name=_('Статус'),
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return str(self.task_student)

    class Meta:
        verbose_name = _('Статус задачи специалиста')
        verbose_name_plural = _('Статус задач специалистов')


class File(Model):
    name = CharField(
        max_length=255,
        verbose_name=_('Имя файла'),
        blank=True,
        null=True,
    )
    file = FileField(
        upload_to='Files',
        verbose_name=_('Файлы')
    )

    def __str__(self):
        if self.name:
            return self.name
        return str(self.pk)

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')


# сигнальная функция присваивает значение для name
# если оно не было задано явно при загрузке файла
@receiver(pre_save, sender=File)
def set_default_name(sender, instance, **kwargs):
    if not instance.name and instance.file:
        instance.name = os.path.basename(instance.file.name)


class DataKnowledgeFree(Model):
    chapter = ForeignKey(
        'Chapter',
        verbose_name=_('Тема'),
        on_delete=CASCADE
    )
    under_section = ForeignKey(
        'UnderSection',
        verbose_name=_('Раздел'),
        on_delete=CASCADE
    )
    files = ManyToManyField(
        'File',
        verbose_name=_('Файлы'),
        blank=True
    )
    video_url = TextField(
        verbose_name=_('Видео-материалы'),
        blank=True,
        null=True
    )
    url = TextField(
        verbose_name=_('Прочие ссылки'),
        blank=True,
        null=True
    )

    def __str__(self):
        if self.chapter and self.chapter.name:
            chapter_name = self.chapter.name
        else:
            chapter_name = 'No Chapter'

        if self.under_section and self.under_section.name:
            under_section_name = self.under_section.name
        else:
            under_section_name = 'No Section'

        return f"{chapter_name} - {under_section_name}"

    class Meta:
        verbose_name = _('База знаний бесплатно')
        verbose_name_plural = _('Базы знаний бесплатно')


class Chapter(Model):
    name = CharField(
        verbose_name=_('Тема'),  # бывший _('Раздел')
        max_length=150
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Тема')  # бывший _('Разделы')
        verbose_name_plural = _('Темы')  # бывший _('Разделы')


class UnderSection(Model):
    name = CharField(
        verbose_name=_('Раздел'),  # бывший _('Под раздел')
        max_length=150
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Раздел Образование')
        verbose_name_plural = _('Раздел Образование')


class DataKnowledge(Model):
    chapter = ForeignKey(
        'Chapter',
        verbose_name=_('Тема'),
        on_delete=CASCADE
    )
    under_section = ForeignKey(
        'UnderSection',
        verbose_name=_('Раздел'),
        on_delete=CASCADE
    )
    files = ManyToManyField(
        'File', verbose_name=_('Файлы'),
        blank=True
    )
    video_url = TextField(
        verbose_name=_('Видео-материалы'),
        blank=True,
        null=True
    )
    url = TextField(
        verbose_name=_('Прочие ссылки'),
        blank=True,
        null=True
    )

    def __str__(self):
        if self.chapter and self.chapter.name:
            chapter_name = self.chapter.name
        else:
            chapter_name = 'No Chapter'

        if self.under_section and self.under_section.name:
            under_section_name = self.under_section.name
        else:
            under_section_name = 'No Section'

        return f"{chapter_name} - {under_section_name}"

    class Meta:
        verbose_name = _('База знаний платно')
        verbose_name_plural = _('Базы знаний платно')


class DataKnowledgeGeneral(Model):
    chapter = ForeignKey(
        Chapter,
        verbose_name=_('Тема'),
        on_delete=CASCADE
    )
    under_section = ForeignKey(
        UnderSection,
        verbose_name=_('Раздел'),
        on_delete=CASCADE
    )
    files = ManyToManyField(
        'File', verbose_name=_('Файлы'),
        blank=True
    )
    video_url = TextField(
        verbose_name=_('Видео-материалы'),
        blank=True,
        null=True
    )
    url = TextField(
        verbose_name=_('Прочие ссылки'),
        blank=True,
        null=True
    )

    def get_data(self):
        data_knowledge_list = []
        for dataknowledge in self.pinned_dataknowledge.all():
            data_knowledge_list.append({
                "chapter_name": (
                    dataknowledge.chapter.name
                    if dataknowledge.chapter
                    else "No Chapter"
                ),
                "under_section_name": (
                    dataknowledge.under_section.name
                    if dataknowledge.under_section
                    else "No Section"
                ),
                "files": (
                    ", ".join(
                        file.name for file in dataknowledge.files.all()
                    ) or "No Files"
                ),
                "video_url": dataknowledge.video_url or "No Video",
                "url": dataknowledge.url or "No URL",
            })
        return data_knowledge_list

    def __str__(self):
        # return self.chapter.name
        if self.chapter and self.chapter.name:
            chapter_name = self.chapter.name
        else:
            chapter_name = 'No Chapter'

        if self.under_section and self.under_section.name:
            under_section_name = self.under_section.name
        else:
            under_section_name = 'No Section'

        return f"{chapter_name} - {under_section_name}"

    class Meta:
        verbose_name = _('База знаний общая')
        verbose_name_plural = _('Базы знаний общие')


class Mailing(Model):
    subject = CharField(
        max_length=225,
        verbose_name=_('Тема')
    )
    title = CharField(
        max_length=255,
        verbose_name=_('Заголовок')
    )
    message = TextField(
        verbose_name=_('Сообщение')
    )
    photo = ImageField(
        verbose_name=_('Фото'),
        null=True,
        blank=True,
        upload_to='img_mailing'
    )
    sent_date = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата отправки')
    )
    student = ManyToManyField(
        'Student',
        related_name='mailings',
        verbose_name=_('Специалисты')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Рассылка')
        verbose_name_plural = _('Рассылки')


class Orders(Model):
    creation_date = DateTimeField(
        auto_now_add=True,
        verbose_name=_('дата создания')
    )
    student = ForeignKey(
        'Student',
        on_delete=CASCADE,
        related_name='orders',
        verbose_name=_('Специалист')
    )
    description = TextField(
        verbose_name=_('Описание')
    )
    amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Сумма')
    )
    payment_status = BooleanField(
        default=False,
        verbose_name=_('Статус оплаты')
    )

    def __str__(self):
        return str(self.student)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')


class ProjectInvitation(Model):
    project = ForeignKey(
        Project,
        on_delete=CASCADE,
        related_name='invitations'
    )
    students = ManyToManyField(
        Student,
        related_name='project_invitations'
    )
    invitation_duration = IntegerField(
        default=2,
        verbose_name=_('Срок действия')
    )
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Создано')
    )
    updated_at = DateTimeField(auto_now=True)

    def is_expired(self):
        return (
            timezone.now()
            > self.created_at
            + timezone.timedelta(days=self.invitation_duration)
        )

    def __str__(self):
        return f"{self.project.name}"

    class Meta:
        verbose_name = _('Приглашение в проект')
        verbose_name_plural = _('Приглашение в проекты')


class StudentInvitation(Model):
    invitation = ForeignKey(
        ProjectInvitation,
        on_delete=CASCADE,
        related_name='student_invitations',
        verbose_name=_('Приглашение')
    )
    student = ForeignKey(
        Student,
        on_delete=CASCADE,
        related_name='student_invitations',
        verbose_name=_('Приглашенный специалист')
    )
    reaction_status = IntegerField(
        default=0,
        verbose_name=_('Статус отклика')
    )  # 0 - не определен; 1 - отказался; 2 - проигнорировал

    def __str__(self):
        return (
            f"Приглашение {self.student.full_name}\n"
            f"в проект {self.invitation.project.name}"
        )

    class Meta:
        verbose_name = _('Приглашение студента')
        verbose_name_plural = _('Приглашение студентов')
