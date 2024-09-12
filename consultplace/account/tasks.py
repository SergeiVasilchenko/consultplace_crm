import logging
import os

import requests
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from dotenv import load_dotenv

from .models import (AnswersStudent, Mailing, Project, ProjectInvitation,
                     TestTaskEvaluation)

logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'


@shared_task
def send_telegram_message_task(chat_id, message, token):
    """
    Функция отправит сообщение о предложенной position в телеграм бот.
    Запускается сигналом update_student_position.
    """
    token = TELEGRAM_TOKEN
    telegram_api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(telegram_api_url, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent to {chat_id}: {message}")
        return {'status': 'success', 'data': response.json()}
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        return {'status': 'error', 'data': str(e)}


@shared_task
def send_bulk_messages(mailing_id):
    """
    Функция принимает id объекта рассылки,
    в котором в цикле для каждого объекта Student,
    прикрепленного к объекту рассылки,
    вызовет celery задачу send_telegram_message
    Запускается сигналом trigger_mailing.
    """
    logger.info(f"Starting to send bulk messages for Mailing ID: {mailing_id}")

    try:
        mailing = Mailing.objects.get(id=mailing_id)
        message = mailing.message
        token = TELEGRAM_TOKEN
        for student in mailing.student.all():
            chat_id = student.telegram_user_id
            send_telegram_message.delay(chat_id, message, token)
            logger.debug(
                f"Queued message for student {student.id}\n"
                f"with chat ID {chat_id}"
            )

    except ObjectDoesNotExist:
        logger.error(f"Mailing with id {mailing_id} does not exist.")
    except Exception as e:
        logger.error(
            f"An error occurred while sending bulk messages: {str(e)}"
        )


@shared_task
def send_telegram_message(chat_id, message, token):
    """
    Функция отправки сообщения в бот каждому юзеру,
    который указан в объекте Mailing массовой рассылки.
    Вызывается для каждого Student в цикле в celery задаче send_bulk_messages.
    """
    logger.debug(f"Sending message to chat ID {chat_id}")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        logger.error(f"Failed to send message to {chat_id}: {response.text}")
    else:
        logger.info(f"Message sent to {chat_id} successfully")
    return response.json()


@shared_task
def schedule_notification_task(test_task_evaluation_id):
    """
    Функция отправит напоминание в телеграм бот объекту Student.
    Напоминание отсылается за 1 сутки до окончиная срока выполнения задания.
    Условие выполнения функуии:
        поле url у TestTaskEvaluation имеет значение,
        отличное от дефолтного.
    """
    try:
        test_task_evaluation = TestTaskEvaluation.objects.get(
            pk=test_task_evaluation_id
        )
    except ObjectDoesNotExist:
        return
    if test_task_evaluation.url:
        return

    chat_id = test_task_evaluation.student.telegram_user_id
    message = (
        f"Привет {test_task_evaluation.student.full_name}!\n"
        "Осталась 1 минута до окончания срока выполнения тестового задания."
    )

    token = TELEGRAM_TOKEN
    telegram_api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(telegram_api_url, json=payload)
        response.raise_for_status()
        return {'status': 'success', 'data': response.json()}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'data': str(e)}


@shared_task
def deadline_notification_task(test_task_evaluation_id):
    """
    Функция отправит уведомление в телеграм бот объекту Student.
    Уведомление сообщит об истечении времени выполнения задания.
    Сообщение о наступлении дедлайна деактивирует кнопку отправки задания.
    Условие выполнения функуии:
        поле url у TestTaskEvaluation имеет значение,
        отличное от дефолтного.
    """
    try:
        test_task_evaluation = TestTaskEvaluation.objects.get(
            pk=test_task_evaluation_id
        )
    except ObjectDoesNotExist:
        return

    # Проверка, если URL уже заполнен, прекращаем выполнение
    if test_task_evaluation.url:
        return

    chat_id = test_task_evaluation.student.telegram_user_id
    message = (
        f"Привет {test_task_evaluation.student.full_name}!\n"
        "К сожалению твое время для сдачи тестовой задачи закончились.\n"
        "По остальным вопросам обращайтесь к @Dariasssa"
    )

    token = TELEGRAM_TOKEN
    telegram_api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': {'remove_keyboard': True},
    }

    try:
        response = requests.post(telegram_api_url, json=payload)
        response.raise_for_status()
        return {'status': 'success', 'data': response.json()}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'data': str(e)}


@shared_task
def invitation_notification(invitation_id):
    try:
        invitation = ProjectInvitation.objects.get(id=invitation_id)
        for student_invitation in invitation.student_invitations.all():
            student = student_invitation.student
            chat_id = student.telegram_user_id
            message = (
                "Вас приглашают принять участие\n"
                f"в проекте: {invitation.project.name}"
            )
            send_telegram_message_invitation(
                chat_id,
                message,
                inline_buttons=[
                    {
                        'text': 'Принять',
                        'callback_data': f'accept_{student_invitation.id}'
                    },
                    {
                        'text': 'Отказаться',
                        'callback_data': f'decline_{student_invitation.id}'
                    }
                ]
            )
    except ObjectDoesNotExist:
        return


@shared_task
def invitation_reminder_notification(invitation_id):
    try:
        invitation = ProjectInvitation.objects.get(id=invitation_id)
        for student_invitation in invitation.student_invitations.filter(
            reaction_status=0
        ):
            student = student_invitation.student
            if student in invitation.project.students.all():
                chat_id = student.telegram_user_id
                message = (
                    "Напоминаем, что у вас осталось 1 сутки\n"
                    "чтобы подтвердить участие\n"
                    f"в проекте: {invitation.project.name}"
                )
                send_telegram_message_invitation(
                    chat_id,
                    message,
                    inline_buttons=[
                        {
                            'text': 'Принять',
                            'callback_data': f'accept_{student_invitation.id}'
                        },
                        {
                            'text': 'Отказаться',
                            'callback_data': f'decline_{student_invitation.id}'
                        }
                    ]
                )
    except ObjectDoesNotExist:
        return


@shared_task
def invitation_deadline_notification(invitation_id):
    try:
        invitation = ProjectInvitation.objects.get(id=invitation_id)
        for student_invitation in invitation.student_invitations.filter(
            reaction_status=0
        ):
            student = student_invitation.student
            # if student in invitation.project.students.all():
            chat_id = student.telegram_user_id
            message = (
                f"Срок приглашения в проект: {invitation.project.name}\n"
                "истек. Набор исполнителей завершен."
            )
            student_invitation.reaction_status = 2  # Procrastinated
            student_invitation.save()
            send_telegram_message_invitation(
                chat_id,
                message
            )
    except ObjectDoesNotExist:
        return


@shared_task
def send_telegram_message_invitation(chat_id, text, inline_buttons=None):
    token = TELEGRAM_TOKEN
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    if inline_buttons:
        reply_markup = {
            'inline_keyboard': [
                [
                    {
                        'text': btn['text'],
                        'callback_data': btn['callback_data']
                    }
                    for btn in inline_buttons
                ]
            ]
        }
        payload['reply_markup'] = reply_markup

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")


@shared_task
def send_project_update_notification(project_id, changes):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return

    students = project.students.all()
    change_details = "\n".join(
        [f"{field}: {old} -> {new}" for field, old, new in changes]
    )
    for student in students:
        chat_id = student.telegram_user_id
        message = (
            f"Произошли изменения в проекте: {project.name}\n"
            "Пожалуйста, проверьте обновления.\n"
            f"Изменения:\n{change_details}"
        )
        send_telegram_message_proj_update.delay(chat_id, message)


@shared_task
def send_telegram_message_proj_update(chat_id, text):
    token = TELEGRAM_TOKEN
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")


@shared_task
def send_telegram_answersstudent_message(
    answer_id,
    message,
    inline_buttons=None
):
    try:
        answer = AnswersStudent.objects.get(id=answer_id)
        student = answer.task.assigned_student
        chat_id = student.telegram_user_id
        payload = {
            'chat_id': chat_id,
            'text': message
        }

        if inline_buttons:
            reply_markup = {
                'inline_keyboard': [
                    [
                        {
                            'text': btn['text'],
                            'callback_data': btn['callback_data']
                        }
                        for btn in inline_buttons
                    ]
                ]
            }

            payload['reply_markup'] = reply_markup

        logger.info(
            f'Sending message to chat_id: {chat_id}, message: {message}'
        )

        response = requests.post(url=TELEGRAM_API_URL, json=payload)

        if response.status_code == 200:
            logger.info(
                f'Message sent successfully to chat_id: {chat_id}'
            )
        else:
            logger.error(
                f'Failed to send message to chat_id: {chat_id}.\n'
                f'Response: {response.status_code}, {response.text}'
            )
    except AnswersStudent.DoesNotExist:
        logger.error(
            f'AnswersStudent with id {answer_id} does not exist.'
        )
    except Exception as e:
        logger.error(
            'An error occurred while sending message\n'
            f'to chat_id: {chat_id}. Error: {str(e)}'
        )


@shared_task
def send_telegram_taskstudent_message(telegram_id, message):
    if telegram_id:
        payload = {
            'chat_id': telegram_id,
            'text': message
        }
        try:
            response = requests.post(TELEGRAM_API_URL, data=payload)
            response.raise_for_status()
            logger.info(
                "Уведомление успешно отправлено студенту"
                f"с Telegram ID {telegram_id}"
            )
        except requests.exceptions.RequestException as e:
            logger.error(
                "Ошибка при отправке сообщения в Telegram студенту"
                f"с Telegram ID {telegram_id}: {e}"
            )
    else:
        logger.warning(
            "Не удалось отправить уведомление: Telegram ID не указан"
        )
