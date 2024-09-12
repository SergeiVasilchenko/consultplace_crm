import logging
import os

from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from dotenv import load_dotenv

from .models import (AnswersStudent, Mailing, Project, ProjectInvitation,
                     Student, StudentInvitation, TaskStudent, TestTask,
                     TestTaskEvaluation)
from .tasks import (deadline_notification_task,
                    invitation_deadline_notification, invitation_notification,
                    invitation_reminder_notification,
                    schedule_notification_task, send_bulk_messages,
                    send_project_update_notification,
                    send_telegram_answersstudent_message,
                    send_telegram_message_task,
                    send_telegram_taskstudent_message)

logger = logging.getLogger(__name__)

load_dotenv()


@receiver(post_save, sender=Student)
def assign_and_send_test_task(sender, instance, created, **kwargs):
    """
    Сигнал создания тестового задания для нового студента.
    Тригер: создание в БД объекта модели Student.
    Сигнал проверяет, если объект вновь создан,
    то из списка объектов TestTask выбирается случайный.
    Выбранный случайно TestTask ассоциируется с Student,
    через создание объекта TestTaskEvaluation.
    Оповещение о предложении тестового задания отправит телеграм бот.
    Изменения в объекте модели TestTaskEvaluation запустят другие сигналы.
    """
    if created:
        test_task = TestTask.objects.order_by('?').first()
        # chat_id = instance.telegram_user_id
        if test_task:
            # message = (
            #     f"Привет {instance.full_name}!\n"
            #     "Благодарим за регистрацию\n"
            #     "Для дальнейшей нашей совместной работы\n"
            #     "нам нужно оценить ваши знания и навыки.\n"
            #     "Предлагаем выполнить тестовое задание\n"
            #     "Описание задания:\n"
            #     f"{test_task.description}\n"
            #     "Срок выполнения (дни):\n"
            #     f"{test_task.task_duration}\n"
            #     "Подробный материал задания по ссылке:"
            #     f"{test_task.url}"
            # )

            # token = os.getenv('BOT_TOKEN')
            # try:
            #     send_telegram_message_task.delay(chat_id, message, token)
            #     logger.info(
            #         f"Sent test task {test_task.title}\n"
            #         f"to student {instance.full_name}\n"
            #         f"at chat ID {chat_id}"
            #     )
            try:
                evaluation_object = TestTaskEvaluation.objects.create(
                    telegram_user_id=instance.telegram_user_id,
                    assigned_testtask=test_task
                )
                logger.info(
                    "Created TestTaskEvaluation\n"
                    f"with ID {evaluation_object.id}"
                    f"for student {instance.full_name}"
                )
                evaluation_object.update_student_position()
            except Exception as e:
                logger.error(
                    f"Failed to send message or create evaluation"
                    f"for {instance.full_name}: {e}"
                )
        else:
            logger.warning(
                "No test task instance available to assign to the student."
            )
    else:
        logger.debug(
            f"Updated student {instance.full_name} but no action needed."
        )


@receiver(post_save, sender=TestTaskEvaluation)
def schedule_notification(sender, instance, created, **kwargs):
    """
    Сигнал обратного отсчета времени выполнения тестового.
    После создания объекта TestTaskEvaluation,
    этот сигнал берет значение task_dutarion у TestTask,
    ассоциированной с Student в TestTaskEvaluation.
    countdown_time - это время выполнения (сек),
    за вычетом 1 суток.
    Ее значение передается аргументом countdown в apply_async,
    которая выполнит задачу schedule_notification_task для celery.
    """
    logger.info(
        "schedule_notification signal triggered\n"
        f"for TestTaskEvaluation id={instance.student.full_name}."
    )
    if created:
        task_duration = instance.assigned_testtask.task_duration
        countdown_time = (task_duration - 1) * 60
        countdown_time_for_deadline = task_duration * 60
        # уведомление за 1 минуту до дедлайна. для теста
        schedule_notification_task.apply_async(
            (instance.pk,),
            countdown=countdown_time
        )
        logger.info(
            "schedule_notification_task activated for reminder before dl."
        )
        # уведомление в момент дедлайна. для теста
        deadline_notification_task.apply_async(
            (instance.pk,),
            countdown=countdown_time_for_deadline
        )
        logger.info(
            "deadline_notification_task activated for deadline notification."
        )


@receiver(post_save, sender=TestTaskEvaluation)
def update_student_position(sender, instance, created, **kwargs):
    """
    Сигнал обновления position у Student.
    Тригер:
        instance.score != 0 ("В работе").
        instance.comment = True (null=False).
        instance.is_completed == 'Нет'
    Проверив выполненное тестовое,
    (поле url записанное в БД через телеграм бота студентом),
    админ пишет сообщение (поле comment) и ставит оценку (score).
    При записи в БД поле position у Student принимает значение,
    соответствующее оценке score.
    Сигнал имеет message,
    которая передается в celery задачу send_telegram_message_task.
    """
    logger.info(
        f"Post save signal triggered for TestTaskEvaluation id={instance.pk}"
    )

    if created:
        logger.info(
            "New TestTaskEvaluation created\n"
            f"with id={instance.pk}, no message sent."
        )
        return

    if (
        (instance.score != 0 and instance.comment)
        and instance.is_completed == 'Нет'
    ):
        logger.info(
            "Score or comment updated for\n"
            f"TestTaskEvaluation id={instance.pk}, score={instance.score}"
        )

        if instance.score == 1:
            new_position = 1
        elif instance.score == 2:
            new_position = 2
        elif instance.score == 3:
            new_position = 3
        else:
            new_position = 0

        student = instance.student
        student.position = new_position
        student.save(update_fields=['position'])

        chat_id = student.telegram_user_id
        message = (
            f"Привет {instance.student.full_name}!\n"
            "Мы проверили вашу работу.\n"
            "Ниже - сообщение от проверяющего:\n"
            f"\"{instance.comment}\"\n"
            f"Мы видим вас в роли: {instance.student.get_position_display()}."
        )
        token = os.getenv('BOT_TOKEN')
        send_telegram_message_task.delay(chat_id, message, token)
        logger.info(
            f"Message sent to {instance.student.full_name}\n"
            "about updated evaluation."
        )
    else:
        logger.info(
            "No relevant fields ('score' or 'comment')\n"
            f"were updated for TestTaskEvaluation id={instance.pk}"
        )


@receiver(post_save, sender=Mailing)
def trigger_mailing(sender, instance, created, **kwargs):
    """
    Сигнал рассылки сообщения для списка Student объекта Mailing.
    Тригер:
        создание объекта Mailing.
    Срабатывает celery задача send_bulk_messages.
    """
    if created:
        send_bulk_messages.delay(instance.id)


@receiver(m2m_changed, sender=ProjectInvitation.students.through)
def create_student_invitations(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        logger.info(
            f"Создание StudentInvitations для ProjectInvitation {instance.id}"
        )
        students = instance.students.filter(pk__in=pk_set)
        print(students)
        for student in students:
            StudentInvitation.objects.create(
                invitation=instance,
                student=student
            )
            logger.info(
                f"Создано StudentInvitation для {student.full_name}"
            )
        countdown_duration = instance.invitation_duration * 60
        # Переводим минуты в секунды
        print(countdown_duration)
        # За 1 сутки (24 часа) до дедлайна в секундах
        reminder_time = countdown_duration - 60
        # Переводим минуты в секунды
        print(reminder_time)

        # Запуск задач Celery
        invitation_notification.apply_async(
            (instance.id,),
            countdown=10
        )
        invitation_reminder_notification.apply_async(
            (instance.id,),
            countdown=reminder_time
        )
        invitation_deadline_notification.apply_async(
            (instance.id,),
            countdown=countdown_duration
        )


@receiver(pre_save, sender=Project)
def track_project_changes(sender, instance, **kwargs):
    """
    Отслеживание изменений полей модели Project перед сохранением.
    """
    try:
        old_instance = Project.objects.get(pk=instance.pk)
    except Project.DoesNotExist:
        old_instance = None

    instance._old_instance = old_instance


@receiver(post_save, sender=Project)
def notify_project_changes(sender, instance, **kwargs):
    """
    Отправка уведомлений студентам проекта при изменении полей.
    """
    if not instance._old_instance:
        return

    # Поля, за изменением которых нужно следить
    tracked_fields = [
        'group', 'captain', 'name', 'intricacy',
        'start_date', 'end_date',
        'group_grade', 'intricacy_coefficient',
        'pinned_dataknowledge'
    ]

    changes = []
    for field in tracked_fields:
        old_value = getattr(instance._old_instance, field)
        new_value = getattr(instance, field)
        if old_value != new_value:
            verbose_name = instance._meta.get_field(field).verbose_name
            old_value = (
                old_value
                if isinstance(old_value, (str, int, float, type(None)))
                else str(old_value)
            )
            new_value = (
                new_value
                if isinstance(new_value, (str, int, float, type(None)))
                else str(new_value)
            )
            changes.append((verbose_name, old_value, new_value))

    if changes:
        logger.info(f"Project {instance.name} has been updated.")
        send_project_update_notification.delay(instance.pk, changes)


@receiver(post_save, sender=AnswersStudent)
def notify_answer_status(sender, instance, created, **kwargs):
    if created:
        return

    if not instance.comment:
        return

    inline_buttons = None
    # if instance.status == 'Suggest edits':
    if instance.status == 1:
        message = (
            "Мы проверили твою работу. Она почти готова, "
            "но нужны кое-какие корректировки. "
            f"Вот комментарий проверяющего: {instance.comment}"
        )
        inline_buttons = [
            {
                'text': 'Послать правки',
                'callback_data': 'send_edits'
            }
        ]

    # elif instance.status == 'Submit feedback':
    elif instance.status == 2:
        message = (
            f"Поздравляем! Работа принята.\n"
            f"Вот комментарий проверяющего: {instance.comment}\n"
            f"Получены оценки:\n"
            f"Оценка по проекту: {instance.personal_grade}\n"
            f"Соблюдение дедлайнов: {instance.deadline_compliance}\n"
            f"Рекомендация менеджера: {instance.manager_recommendation}\n"
            f"Коэффициент сложности: {instance.intricacy_coefficient}\n"
            f"Кредиты: {instance.task_credits}"
        )
    else:
        return
    send_telegram_answersstudent_message.delay(
        instance.id,
        message,
        inline_buttons=inline_buttons
    )


@receiver(m2m_changed, sender=TaskStudent.pinned_dataknowledge.through)
def notify_student_on_task_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        try:
            task_data = instance.to_dict()

            message = (
                f"Привет, вам назначена задача: {task_data['title']}\n"
                f"Проект: {task_data['project']}\n"
                f"Описание: {task_data['description']}\n"
                f"Примечание: {task_data['notice']}\n"
                f"Материалы: {task_data['material']}\n"
                f"Дата начала: {task_data['start_date']}\n"
                f"Дата окончания: {task_data['end_date']}\n"
                f"Методология:\n"
            )

            if task_data['pinned_dataknowledge']:
                for dataknowledge in task_data['pinned_dataknowledge']:
                    message += (
                        f"- Тема: {dataknowledge['chapter_name']}\n"
                        f"-  Раздел: {dataknowledge['under_section_name']}\n"
                        f"-  Файлы: {dataknowledge['files']}\n"
                        f"-  Видео: {dataknowledge['video_url']}\n"
                        f"-  Ссылки: {dataknowledge['url']}\n"
                    )
            else:
                message += "Нет данных\n"

            logger.info(
                f"Отправка сообщения в Telegram для студента ID "
                f"{instance.assigned_student.telegram_user_id}: {message}"
            )

            send_telegram_taskstudent_message.delay(
                instance.assigned_student.telegram_user_id,
                message
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Telegram: {e}")
