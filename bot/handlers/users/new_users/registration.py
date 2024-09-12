import logging
from re import match

import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from data.config import URL_BASE
from db_responce import log_get, log_post, log_put
from email_validator import validate_email
from filters import IsNewUser, IsPrivate
from keyboards.default import kb_start, new_kb_start, send_test_task
from keyboards.inline import (ikb_acc_1_stage, ikb_acc_2_stage,
                              ikb_acc_3_stage, ikb_cancel, ikb_reg_1_stage,
                              ikb_reg_2_stage, ikb_reg_3_stage, ikb_sex)
from loader import dp
from special_fuc import edit_message


class RegState(StatesGroup):
    fio = State()
    phone = State()
    mail = State()
    age = State()
    sex = State()
    work_time = State()
    student_cv = State()
    faculty = State()
    interests = State()
    nishi = State()
    goals = State()
    education = State()
    university = State()
    course = State()
    check = State()
    user_option = State()
    cancel = State()


def rrs(string):
    return string.replace('<b>', '').replace('</b>', '').strip()


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def account_text(data):
    text = f'''
<b>Personal account</b>
Here you can edit your personal data.

Full name: {data["fio"]}
Age: {data["age"]}
Sex: {data["sex"]}
Phone: {data["phone"]}
Mail: {data["mail"]}
Workload: {data['work_time']}
CV: {data['student_cv']}

Education: {data["reg_education"][0]}
University: ({data["reg_university"][0] if len(data["reg_university"]) == 1 else data["reg_university"]})
Faculty: {data["faculty"]}
Course: {data["reg_course"][0]}

Interests: {', '.join(data['reg_interests'] + ([data['user_reg_interests']] if data['user_reg_interests'] else []))}
Niches: {', '.join(data['reg_nishi'] + ([data['user_reg_nishi']] if data['user_reg_nishi'] else []))}
Goals: {', '.join(data['reg_goal'] + ([data['user_reg_goal']] if data['user_reg_goal'] else []))}
'''
    return text


def status_text_1_stage(data):
    text = f'''<b>Stage 1 of 3</b>:
Fill in your personal data, this is very important, because it is important for us to understand who we are helping😊\n
 *Full name: {data["fio"]}
 *Age: {data["age"]}
 *Sex: {data["sex"]}
 *Phone: {data["phone"]}
 *Mail: {data["mail"]}
 *Workload: {data['work_time']}'''

    return text


def status_text_2_stage(data):
    text = f'''<b>Этап 2 из 3</b>
If you are studying (university, college) or have already graduated, be sure to specify the data on education, otherwise put dashes.\n
 *Education: {data["reg_education"][0]}
 *University: {data["reg_university"][0] if len(data["reg_university"]) == 1 else data["reg_university"]}
 *Faculty: {data["faculty"]}
 *Course: {data["reg_course"][0]}'''

    return text


def status_text_3_stage(data):
    text = f'''<b>Этап 3 из 3</b>
Indicate your goals and interests so that we can connect you with people who will be interesting to you\n
 Interests: {', '.join(data['reg_interests'] + ([data['user_reg_interests']] if data['user_reg_interests'] else []))}

 Niches: {', '.join(data['reg_nishi'] + ([data['user_reg_nishi']] if data['user_reg_nishi'] else []))}

 Goals: {', '.join(data['reg_goal'] + ([data['user_reg_goal']] if data['user_reg_goal'] else []))}'''

    return text


# новый пользователь регистрируется в боте
@dp.message_handler(IsNewUser(), IsPrivate(), text='Registration')
async def registration_func(message: types.Message, state: FSMContext):
    await RegState.check.set()  # state to make sure we procedure the registration correctly
    async with state.proxy() as data:  # изменить обязательные поля
        data['fio'] = ''
        data['mail'] = ''
        data['age'] = ''
        data['phone'] = ''
        data['sex'] = ''
        data['faculty'] = ''
        data['reg_education'] = ['']
        data['reg_university'] = ['']
        data['reg_course'] = ['']
        data['work_time'] = ''

        data["reg_interests"] = []
        data['user_reg_interests'] = ''
        data["reg_interests_ids"] = []
        data["reg_nishi"] = []
        data["user_reg_nishi"] = ''
        data["reg_nishi_ids"] = []
        data["reg_goal"] = []
        data["user_reg_goal"] = ''
        data["reg_goal_ids"] = []

        data['registration'] = 1
        await message.answer(text="Registration will take place in three stages\nthe first two stages are mandatory, "
                                  "they are marked with an asterisk (*)\n"
                                  "Answer honestly so that we can offer relevant information for you \n"
                                  "Your data is securely (not) protected")
        msg = await message.answer(text=status_text_1_stage(data), reply_markup=ikb_reg_1_stage)
        data['message_id'] = msg.message_id
        data['message_txt'] = msg.text


@dp.message_handler(IsNewUser(), IsPrivate(), commands=['skipAll_26'], state='*')
async def skip_all_reg(message: types.Message, state: FSMContext):
    test_res_bu = log_get(url=f'{URL_BASE}/user_before_university/')
    test_res_u = log_get(url=f'{URL_BASE}/user_university/')
    test_res_c = log_get(url=f'{URL_BASE}/courses/')
    parameters = {
        "full_name": 'test',
        "mobile_phone": '+79999999999',
        "email": 'test@mail.com',
        "tg_nickname": f'{message.from_user.username}',
        "age": 22,
        "gender": 'male',
        "faculty": 'test',
        "manager_status": 'Manager Lead',
        "education_status": 'Base',
        "hours_per_week": 22,
        "telegram_user_id": message.from_user.id,
        "before_university": test_res_bu[0]['id'],
        "university": test_res_u[0]['id'],
        "course": test_res_c[0]['id'],
    }

    res = log_post(url=f'{URL_BASE}/create/', json_=parameters)
    if res:
        text = ('skipped\nAccess is granted, please take the test so that we can assess your level\n '
                'https://docs.google.com/document/d/1XFu9qvZjnqGgqoeP0RRwYFXymsUK_nrKOC_pmwo7o7k/edit')
    else:
        text = 'error'
    await message.answer(text=text, reply_markup=kb_start)
    await state.reset_state()
    await state.finish()


@dp.message_handler(IsNewUser(), IsPrivate(), commands=['skip1_56'], state=RegState.check)
async def skip_1_reg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = 'test'
        data['phone'] = '+79999999999'
        data['mail'] = 'test@mail.com'
        data['age'] = '22'
        data['sex'] = 'male'
        data['work_time'] = '22'
        text = 'skipped first stage\n' + status_text_2_stage(data)

    await edit_message(state=state, chat_id=message.from_user.id,
                       text=text,
                       reply_markup=ikb_reg_2_stage)


@dp.message_handler(IsNewUser(), IsPrivate(), commands=['skip2_45'], state=RegState.check)
async def skip_2_reg(message: types.Message, state: FSMContext):
    test_res_bu = log_get(url=f'{URL_BASE}/user_before_university/')
    test_res_u = log_get(url=f'{URL_BASE}/user_university/')
    test_res_c = log_get(url=f'{URL_BASE}/courses/')

    async with state.proxy() as data:
        data['reg_education_ids'] = [test_res_bu[0]['id']]
        data['reg_university_ids'] = [test_res_u[0]['id']]
        data['reg_course_ids'] = [test_res_c[0]['id']]
        data['faculty'] = 'test'
        text = 'skipped second stage\n' + status_text_3_stage(data)

    await edit_message(state=state, chat_id=message.from_user.id,
                       text=text,
                       reply_markup=ikb_reg_3_stage)


# сообщение для зарегистрированных пользователей, которые вводят Регистрация
@dp.message_handler(IsPrivate(), text='Регистрация')
async def registration_func(message: types.Message):
    await message.answer(text='You are already registered.', reply_markup=kb_start)


# заполнение ФИО
@dp.callback_query_handler(text='reg_fio', state=RegState.check)
async def reg_fio_button(call: types.CallbackQuery):
    await RegState.fio.set()
    await dp.bot.send_message(call.from_user.id, 'Send me your full name\nFormat: John Jonah Jameson')


# заполнение телефон
@dp.callback_query_handler(text='reg_phone', state=RegState.check)
async def reg_fio_button(call: types.CallbackQuery):
    await RegState.phone.set()
    await dp.bot.send_message(call.from_user.id, text='Send me the phone\nFormat: +79876543210')


# заполнение почты
@dp.callback_query_handler(text='reg_mail', state=RegState.check)
async def reg_mail_button(call: types.CallbackQuery):
    await RegState.mail.set()
    await dp.bot.send_message(call.from_user.id, text='Send me your mail\nFormat: mail@domen.com')


# заполнение возраста
@dp.callback_query_handler(text='reg_age', state=RegState.check)
async def reg_fio_button(call: types.CallbackQuery):
    await RegState.age.set()
    await dp.bot.send_message(call.from_user.id, text='Send me your age\nFormat: 25')


# заполнение факультета
@dp.callback_query_handler(text="reg_faculty", state=RegState.check)
async def reg_faculty_button(call: types.callback_query):
    await RegState.faculty.set()
    await dp.bot.send_message(call.from_user.id, text='Send me the name of your faculty\nFormat: Economy')


# редактирование пола
@dp.callback_query_handler(text="reg_sex", state=RegState.check)
async def reg_sex_button(call: types.CallbackQuery):
    await RegState.sex.set()
    await dp.bot.send_message(chat_id=call.from_user.id, text='Indicate your gender.', reply_markup=ikb_sex)
    #  нахуй пидорасов и прочую нечисть


# редактирование часов работы
@dp.callback_query_handler(text="reg_work_time", state=RegState.check)
async def reg_work_time_button(call: types.CallbackQuery):
    await RegState.work_time.set()
    await dp.bot.send_message(chat_id=call.from_user.id,
                              text='How many hours a week are you ready to devote to the project\nFormat: 40')


# заполнение текстовых полей
@dp.message_handler(
    state=[RegState.fio, RegState.phone, RegState.age, RegState.faculty, RegState.mail, RegState.work_time])
async def reg_get_fio(message: types.Message, state: FSMContext):
    now_state = await state.get_state()
    now_state = now_state[9:]
    if now_state != 'mail' or validate_email(message.text, check_deliverability=False):
        if now_state != 'age' or is_integer(message.text):  # проверка на заполнение возраста целым числом
            if (now_state != 'age') or ((14 <= int(message.text)) and (int(message.text) <= 100)):
                if (
                    (now_state != 'phone')
                    or match(
                        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                        message.text
                    )
                ):
                    async with state.proxy() as data:
                        data[f'{now_state}'] = message.text
                        await RegState.check.set()

                        if data['registration'] == 0:  # не регистрация
                            msg = await message.answer(text=account_text(data), reply_markup=(
                                ikb_acc_1_stage if now_state != 'faculty' else ikb_acc_2_stage))
                        else:
                            text = status_text_1_stage(data) if now_state != 'faculty' else status_text_2_stage(data)
                            reply_markup = ikb_reg_1_stage if now_state != 'faculty' else ikb_reg_2_stage
                            msg = await message.answer(text=text, reply_markup=reply_markup)

                        try:
                            await dp.bot.delete_message(message.from_user.id, data['message_id'])
                        except Exception as ex:
                            logging.error(ex)
                        data['message_id'] = msg.message_id
                        data['message_txt'] = msg.text
                else:
                    await message.answer(text="Please enter your correct phone number in the specified format.")
            else:
                await message.answer(text="Please enter your correct age.")
        else:
            await message.answer(text="Enter your age as a number, please.")
    else:
        await message.answer(text="Check the correctness of the entered e-mail.\nSend the correct e-mail.")


# выбор пола
@dp.callback_query_handler(text=["male", 'female'], state=RegState.sex)
async def sex(call: types.CallbackQuery, state: FSMContext):
    await RegState.check.set()
    async with state.proxy() as data:
        if call.data == 'male':
            data['sex'] = 'Male'
        elif call.data == 'female':
            data['sex'] = 'Female'

        try:
            await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        except Exception as ex:
            logging.error(ex)

        if data['registration'] == 0 and data['message_txt'] != rrs(account_text(data)):
            msg = await dp.bot.edit_message_text(text=account_text(data),
                                                 chat_id=call.from_user.id,
                                                 message_id=data['message_id'],
                                                 reply_markup=ikb_acc_1_stage)
            data['message_txt'] = msg.text
        elif data['registration'] == 1 and data['message_txt'] != rrs(status_text_1_stage(data)):
            msg = await dp.bot.edit_message_text(text=status_text_1_stage(data),
                                                 chat_id=call.from_user.id,
                                                 message_id=data['message_id'],
                                                 reply_markup=ikb_reg_1_stage)
            data['message_txt'] = msg.text


# переход на 2 этап регистрации, в ьлм числе с 3 этапа
@dp.callback_query_handler(text=["reg_next_stage_1", "reg_prev_stage_2"], state=RegState.check)
async def next_stage_1(call: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        if (data['fio'] and data['mail'] and data['age'] and data['phone'] and data['sex'] and data['work_time']) or (
                call.data == "reg_prev_stage_2"):
            try:
                if data['message_txt'] != status_text_2_stage(data).replace('<b>', '').replace('</b>', ''):
                    msg = await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                         message_id=data['message_id'],
                                                         text=status_text_2_stage(data),
                                                         reply_markup=ikb_reg_2_stage)

            except Exception as ex:
                logging.error(ex)
                msg = await call.message.answer(text=status_text_2_stage(data), reply_markup=ikb_reg_2_stage)
            data['message_txt'] = msg.text
        else:
            await call.answer(text='Fill in all required fields to proceed to the next stage.')


@dp.callback_query_handler(text="reg_prev_stage_2", state=RegState.check)
async def prev_stage_2(call: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        try:
            if data['message_txt'] != status_text_1_stage(data).replace('<b>', '').replace('</b>', ''):
                msg = await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                     message_id=data['message_id'],
                                                     text=status_text_1_stage(data),
                                                     reply_markup=ikb_reg_1_stage)

        except Exception as ex:
            logging.error(ex)
            msg = await call.message.answer(text=status_text_1_stage(data), reply_markup=ikb_reg_1_stage)
        data['message_txt'] = msg.text


@dp.callback_query_handler(text="reg_next_stage_2", state=RegState.check)
async def next_stage_2(call: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        if data['faculty'] and data['reg_education'] and data['reg_university'] and data['reg_course']:
            try:
                if data['message_txt'] != status_text_3_stage(data).replace('<b>', '').replace('</b>', ''):
                    msg = await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                         message_id=data['message_id'],
                                                         text=status_text_3_stage(data),
                                                         reply_markup=ikb_reg_3_stage)

            except Exception as ex:
                logging.error(ex)
                msg = await call.message.answer(text=status_text_3_stage(data), reply_markup=ikb_reg_3_stage)
            data['message_txt'] = msg.text
        else:
            await call.answer(text='Fill in all required fields to proceed to the next stage.')


# создание голосования (опроса)
@dp.callback_query_handler(text=['reg_goal', 'reg_interests', 'reg_nishi',
                                 'reg_education', 'reg_course', 'reg_university'], state=RegState.check)
async def change_interests_button(call: types.CallbackQuery, state: FSMContext):
    mult = 0  # флаг на multiple ответы
    url = ''
    if call.data == 'reg_interests':
        mult = 1
        url = f'{URL_BASE}/user_interests_first/'
    elif call.data == 'reg_nishi':
        mult = 1
        url = f'{URL_BASE}/user_interests_second/'
    elif call.data == 'reg_goal':
        mult = 1
        url = f'{URL_BASE}/user_interests_third/'
    elif call.data == 'reg_education':
        url = f'{URL_BASE}/user_before_university/'
    elif call.data == 'reg_course':
        url = f'{URL_BASE}/courses/'
    elif call.data == 'reg_university':
        url = f'{URL_BASE}/user_university/'

    try:
        resp = log_get(url=url)
        if mult:
            options = {i["interest"]: i["id"] for i in resp}
            options['Другое (свой вариант)'] = -1
        else:
            options = {i["name"]: i["id"] for i in resp}
        question = 'Choose up to THREE options from the suggested ones' if mult else 'Choose one of the options'
        poll = await dp.bot.send_poll(chat_id=call.from_user.id,
                                      question=question,
                                      options=list(options.keys()),
                                      is_anonymous=False,
                                      allows_multiple_answers=mult)
    except Exception as ex:
        logging.error(ex)
        await call.message.answer(
            text='I think we have something broken. We apologize for the inconvenience! We are already working on it.')
        return 0

    async with state.proxy() as data:
        data[f'user_{call.data}'] = ''
        data['poll_id'] = poll.message_id
        data['poll_info'] = options
        data['pool_flag'] = call.data


# отработка ответов на опросы
@dp.poll_answer_handler()
async def poll_funk(poll_answer: types.PollAnswer):
    flag = 1  # флаг на выбор пункта Другое
    text = 0  # если текст не поменялся, то ничего не отправлять (используется как флаг)
    state = FSMContext(chat=poll_answer.user.id, storage=dp.storage, user=poll_answer.user.id)
    async with (state.proxy() as data):
        try:
            await dp.bot.delete_message(chat_id=poll_answer.user.id, message_id=data['poll_id'])
        except Exception as ex:
            logging.error(ex)

        answer = []
        names = list(data['poll_info'].keys())
        option_ids = []

        # не больше 3 вариантов
        for option_id in poll_answer.option_ids:
            name = names[option_id]
            answer.append(name)
            option_ids.append(data['poll_info'][name])
            if len(answer) == 3:
                break

        if 'Другое (свой вариант)' in ''.join(answer):
            await dp.bot.send_message(chat_id=poll_answer.user.id, text='Submit your version')
            await RegState.user_option.set()
            answer.pop(-1)
            option_ids.pop(-1)
            flag = 0

        data[data['pool_flag']] = answer
        data[data['pool_flag'] + '_ids'] = option_ids

        # чтобы при выборе другое сообщение со статусом регистрации или лк не обновлялось до того как отправиться свой
        # вариант от пользователя
        if flag:
            # если в лк и текст сообщения изменился
            if data['registration'] == 0 \
                    and data['message_txt'] != account_text(data).replace('<b>', '').replace('</b>', ''):
                text = account_text(data)
                reply_markup = ikb_acc_2_stage if data['pool_flag'] in ['reg_education', 'reg_course',
                                                                        'reg_university'] else ikb_acc_3_stage
            # если на второй стадии (образование) регистрации и текст сообщения поменялся
            elif data['pool_flag'] in ['reg_education', 'reg_course', 'reg_university'] \
                    and data['message_txt'] != status_text_2_stage(data).replace('<b>', '').replace('</b>', ''):
                reply_markup = ikb_reg_2_stage
                text = status_text_2_stage(data)
            # если на третьей стадии (интересы) регистрации и текст сообщения поменялся
            elif data['pool_flag'] in ['reg_goal', 'reg_interests', 'reg_nishi'] \
                    and data['message_txt'] != status_text_3_stage(data).replace('<b>', '').replace('</b>', ''):
                text = status_text_3_stage(data)
                reply_markup = ikb_reg_3_stage
            if text:
                try:
                    msg = await dp.bot.edit_message_text(text=text,
                                                         chat_id=poll_answer.user.id,
                                                         message_id=data['message_id'],
                                                         reply_markup=reply_markup)
                except aiogram.utils.exceptions.MessageIdInvalid as ex:
                    msg = await dp.bot.send_message(chat_id=poll_answer.user.id,
                                                    text=text,
                                                    reply_markup=reply_markup)
                    logging.error(ex)
                data['message_txt'] = msg.text


# добавить свой вариант (Другое)
@dp.message_handler(state=RegState.user_option)
async def user_var(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["pool_flag"] != 'reg_university':
            data[f'user_{data["pool_flag"]}'] = message.text
        else:
            data['reg_university'] = message.text  # 'Другой'

        if data["pool_flag"] == 'reg_university':
            if data['registration'] == 0:
                msg = await message.answer(text=account_text(data),
                                           reply_markup=ikb_acc_2_stage)
            else:
                msg = await message.answer(text=status_text_2_stage(data),
                                           reply_markup=ikb_reg_2_stage)
        else:
            if data['registration'] == 0:
                msg = await message.answer(text=account_text(data),
                                           reply_markup=ikb_acc_3_stage)
            else:
                msg = await message.answer(text=status_text_3_stage(data),
                                           reply_markup=ikb_reg_3_stage)
        try:
            await dp.bot.delete_message(message.from_user.id, data['message_id'])
        except Exception as ex:
            logging.error(ex)
            # надо ведь все равно новый message_id записать?
        data['message_id'] = msg.message_id

    await RegState.check.set()


# отправка
@dp.callback_query_handler(text='reg_send', state=RegState.check)
async def reg_send_to_db(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        parameters = {
            "full_name": data['fio'],
            "mobile_phone": data['phone'],
            "email": data['mail'],
            "tg_nickname": f'{call.from_user.username}',
            "age": int(data['age']),
            "gender": data['sex'],
            "faculty": data['faculty'],
            "manager_status": 'Manager Lead',
            "education_status": 'Base',
            "hours_per_week": int(data['work_time']),
            "telegram_user_id": call.from_user.id,
            "before_university": data['reg_education_ids'][0],
            "university": data['reg_university_ids'][0],
            "course": data['reg_course_ids'][0],
            "interest_first": data["reg_interests_ids"],
            "other_interest_first": data["user_reg_interests"],
            "interest_second": data["reg_nishi_ids"],
            "other_interest_second": data["user_reg_nishi"],
            "interest_third": data["reg_goal_ids"],
            "other_interest_third": data["user_reg_goal"],

            # f"full_name_{REGION_FLAG}": data['fio'],
            # f"mobile_phone_{REGION_FLAG}": data['phone'],
            # f"email_{REGION_FLAG}": data['mail'],
            # f"tg_nickname_{REGION_FLAG}": f'{call.from_user.username}',
            # f"age_{REGION_FLAG}": int(data['age']),
            # f"gender_{REGION_FLAG}": data['sex'],
            # f"faculty_{REGION_FLAG}": data['faculty'],
            # f"manager_status_{REGION_FLAG}": 'Manager Lead',
            # f"education_status_{REGION_FLAG}": 'Base',
            # f"hours_per_week_{REGION_FLAG}": int(data['work_time']),
            # f"telegram_user_id_{REGION_FLAG}": call.from_user.id,
            # f"before_university_{REGION_FLAG}": data['reg_education_ids'][0],
            # f"university_{REGION_FLAG}": data['reg_university_ids'][0],
            # f"course_{REGION_FLAG}": data['reg_course_ids'][0],
            # f"interest_first_{REGION_FLAG}": data["reg_interests_ids"],
            # f"other_interest_first_{REGION_FLAG}": data["user_reg_interests"],
            # f"interest_second_{REGION_FLAG}": data["reg_nishi_ids"],
            # f"other_interest_second_{REGION_FLAG}": data["user_reg_nishi"],
            # f"interest_third_{REGION_FLAG}": data["reg_goal_ids"],
            # f"other_interest_third_{REGION_FLAG}": data["user_reg_goal"],
        }

        # with open('js.json', 'w') as file:
        #     json.dump(parameters, file)

        if data['registration']:  # регистрация
            res = log_post(url=f'{URL_BASE}/create/', json_=parameters)
            test_res = log_get(url=f'{URL_BASE}/testtaskscores/')
            text = 'error'
            for item in test_res:
                if item['telegram_user_id'] == call.from_user.id:
                    text_test_res = log_get(url=f'{URL_BASE}/testtasks/')
                    for test_tasks in text_test_res:
                        if test_tasks['id'] == item['assigned_testtask']:
                            text = (f'{test_tasks["title"]}\n\n'
                                    f'{test_tasks["description"]}\n'
                                    f'Ссылка: {test_tasks["url"]}\n'
                                    f'Прикрепите ссылку на решение.\nВаш ответ:')
                            break
                    break
            await state.update_data(test_task_text=text)
            await state.update_data(test_task_answer='')
            reply_markup = send_test_task
            message_id = data['message_id']
            await state.reset_state(with_data=False)
        else:  # редактирование лк
            res = log_put(url=f'{URL_BASE}/detail-update/{call.from_user.username}/',
                          json_=parameters)
            text = 'Data saved'
            reply_markup = kb_start
            message_id = data['message_id']
            await state.reset_state()
            await state.finish()
        if res:
            # временно !!
            msg = await call.message.answer(text=text, reply_markup=reply_markup)
            await state.update_data(message_id=msg.message_id)
            try:
                await dp.bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
            except Exception as ex:
                logging.error(ex)
        else:
            await call.message.answer(
                text='I think we have something broken. We apologize for the inconvenience! '
                     'We are already working on it.')


@dp.callback_query_handler(text="reg_cancel", state=RegState.check)
async def reg_cancel_check(call: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        await dp.bot.send_message(chat_id=call.from_user.id,
                                  text=f"Cancellation of registration will erase the data already entered."
                                       f"\nCancel {'registration' if data['registration'] else 'editing'}?",
                                  reply_markup=ikb_cancel)
    await RegState.cancel.set()


@dp.callback_query_handler(text="reg_stay", state=RegState.cancel)
async def reg_stay(call: types.CallbackQuery):
    await RegState.check.set()
    try:
        await dp.bot.delete_message(call.from_user.id, call.message.message_id)
    except Exception as ex:
        logging.error(ex)


@dp.callback_query_handler(text='reg_cancel_true', state=RegState.cancel)
async def reg_cancel(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['registration']:
            await call.message.answer(
                text='Registration canceled. To use the features of the bot, you need to register',
                reply_markup=new_kb_start)
        else:
            await dp.bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                               text='Changes are not saved')
            await call.message.answer(text='Main Menu', reply_markup=kb_start)
        await dp.bot.delete_message(call.from_user.id, data['message_id'])

    await state.reset_state()
    await state.finish()

# files = {'file': open('new_test.txt', 'rb')}
# url = 'http://194.67.86.225/ru/api/students/create-student-cv/forkandart'
# response = requests.post(url, data={"student": 30}, files=files)
#
# print(response)
