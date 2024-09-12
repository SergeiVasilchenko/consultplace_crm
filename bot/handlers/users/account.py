# import logging
from urllib.parse import unquote

import requests
from aiogram import types
from data.config import REGION_FLAG, URL_BASE
from db_responce import log_get, log_patch, log_post
from filters import IsPrivate
from keyboards.default import kb_start
from keyboards.inline import (ikb_acc_1_stage, ikb_acc_2_stage,
                              ikb_acc_3_stage, kb_manage)
from loader import dp
from special_fuc import del_message, edit_message

from .new_users.registration import FSMContext, RegState, account_text


def my_filter(in_data: dict, my_ids: list, key: str):
    result = []
    for item in in_data:
        if item['id'] in my_ids:
            result.append(item[key])
    if result:
        return result
    else:
        return []


# TODO projects and tasks
@dp.message_handler(IsPrivate(), text='Personal account')
async def acc_start(message: types.Message, state: FSMContext):
    await RegState.check.set()
    res = log_get(url=f'{URL_BASE}/detail-update/{message.from_user.username}/')
    if res:
        with requests.Session() as sess:
            course_resp = log_get(session=sess, url=f'{URL_BASE}/courses/')
            university_resp = log_get(session=sess, url=f'{URL_BASE}/user_university/')
            before_university_resp = log_get(session=sess,
                                             url=f'{URL_BASE}/user_before_university/')
            first_int_resp = log_get(session=sess, url=f'{URL_BASE}/user_interests_first/')
            second_int_resp = log_get(session=sess, url=f'{URL_BASE}/user_interests_second/')
            third_int_resp = log_get(session=sess, url=f'{URL_BASE}/user_interests_third/')
            student_cv_resp = log_get(session=sess,
                                      url=f'{URL_BASE}/student_cv/{message.from_user.id}/')
        async with state.proxy() as data:
            data['fio'] = res["full_name"]
            data['mail'] = res["email"]
            data['age'] = f'{res["age"]}'
            data['phone'] = res["mobile_phone"]
            data['sex'] = res["gender"]
            data['work_time'] = f'{res["hours_per_week"]}'
            data['faculty'] = res["faculty"]
            data['reg_education_ids'] = [res["before_university"]]
            data['reg_education'] = my_filter(before_university_resp, data['reg_education_ids'], 'name')
            data['reg_university_ids'] = [res["university"]]
            data['reg_university'] = my_filter(university_resp, data['reg_university_ids'], 'name')
            data['reg_course_ids'] = [res["course"]]
            data['reg_course'] = my_filter(course_resp, data['reg_course_ids'], 'name')

            data['reg_interests_ids'] = res["interest_first"]
            data['reg_interests'] = my_filter(first_int_resp, data['reg_interests_ids'], 'interest')
            data["user_reg_interests"] = res["other_interest_first"]
            data['reg_nishi_ids'] = res["interest_second"]
            data['reg_nishi'] = my_filter(second_int_resp, data['reg_nishi_ids'], 'interest')
            data["user_reg_nishi"] = res["other_interest_second"]
            data['reg_goal_ids'] = res["interest_third"]
            data['reg_goal'] = my_filter(third_int_resp, data['reg_goal_ids'], 'interest')
            data["user_reg_goal"] = res["other_interest_third"]

            data['student_cv'] = unquote(student_cv_resp['file'][38:]) if student_cv_resp else ''

            msg = await dp.bot.send_message(chat_id=message.from_user.id, text=account_text(data),
                                            reply_markup=kb_manage)
            data['message_id'] = msg.message_id
            data['message_txt'] = msg.text
            data['registration'] = 0


@dp.callback_query_handler(text="reg_cv", state=RegState.check)
async def reg_work_time_button(call: types.CallbackQuery):
    await RegState.student_cv.set()
    await dp.bot.send_message(chat_id=call.from_user.id,
                              text='Send me a pdf or doc file')


# добавление резюме
@dp.message_handler(state=RegState.student_cv, content_types=types.ContentTypes.DOCUMENT)
async def reg_cv_button(message: types.ContentTypes.DOCUMENT, state: FSMContext):
    file = message.document  # получение дока
    file_name = file['file_name']

    file_info = await dp.bot.get_file(file.file_id)
    file = await dp.bot.download_file(file_info.file_path)  # преобразование в битовую последовательность

    file.name = file_name
    res = log_get(url=f'{URL_BASE}/detail-update/{message.from_user.username}/')
    if res:
        async with state.proxy() as state_data:
            files = {'file': file,
                     f'file_{REGION_FLAG}': file}
            data = {"student": res['id'],
                    f"student_{REGION_FLAG}": res['id']}
            if state_data['student_cv']:  # если файл уже существует
                cv_resp = log_patch(url=f'{URL_BASE}/student_cv/{message.from_user.id}/',
                                    data=data, files=files)
            else:                         # если грузиться впервые
                cv_resp = log_post(url=f'{URL_BASE}/create-student-cv/{message.from_user.id}',
                                   data=data, files=files)
            if cv_resp:
                state_data['student_cv'] = file_name
                text = account_text(state_data)
            else:
                text = 'We have something broken, please try again later'

            msg = await message.answer(text=text, reply_markup=kb_manage)
            # try:
            #     await dp.bot.delete_message(message.from_user.id, state_data['message_id'])
            # except Exception as ex:
            #     logging.error(ex)
            await del_message(state=state, chat_id=message.from_user.id)
            state_data['message_id'] = msg.message_id
            state_data['message_txt'] = msg.text
    await RegState.check.set()


@dp.callback_query_handler(text='acc_back', state=RegState.check)
async def acc_back(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_message(state=state, chat_id=call.from_user.id, text=account_text(data), reply_markup=kb_manage)
    # async with state.proxy() as data:
    #     try:
    #         await dp.bot.edit_message_text(chat_id=call.from_user.id, text=account_text(data),
    #                                        reply_markup=kb_manage, message_id=data['message_id'])
    #     except Exception as ex:
    #         logging.error(ex)
    #         await call.message.answer(text=account_text(data), reply_markup=kb_manage)


@dp.callback_query_handler(text='basic_acc_edit', state=RegState.check)
async def acc_edit_1(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_message(state=state, chat_id=call.from_user.id, text=account_text(data), reply_markup=ikb_acc_1_stage)
    # async with state.proxy() as data:
    #     await dp.bot.edit_message_text(chat_id=call.from_user.id, message_id=data['message_id'],
    #                                    text=account_text(data), reply_markup=ikb_acc_1_stage)


@dp.callback_query_handler(text='edu_acc_edit', state=RegState.check)
async def acc_edit_2(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_message(state=state, chat_id=call.from_user.id, text=account_text(data), reply_markup=ikb_acc_2_stage)
    # async with state.proxy() as data:
    #     await dp.bot.edit_message_text(chat_id=call.from_user.id, message_id=data['message_id'],
    #                                    text=account_text(data), reply_markup=ikb_acc_2_stage)


@dp.callback_query_handler(text='int_acc_edit', state=RegState.check)
async def acc_edit_3(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_message(state=state, chat_id=call.from_user.id, text=account_text(data), reply_markup=ikb_acc_3_stage)
    # async with state.proxy() as data:
    #     await call.message.edit_text(text=account_text(data), reply_markup=ikb_acc_3_stage)


@dp.callback_query_handler(text='cancel_acc', state=RegState.check)
async def acc_cancel(call: types.CallbackQuery, state: FSMContext):
    # async with state.proxy() as data:
    #     try:
    #         await dp.bot.delete_message(call.from_user.id, data['message_id'])
    #     except Exception as ex:
    #         logging.error(ex)
    await del_message(state=state, chat_id=call.from_user.id)
    chat_response = await state.get_data()
    chat_response = chat_response.get('chat_response')
    await state.reset_state()
    await state.finish()
    await state.update_data(chat_response=chat_response)
    await call.message.answer(text='Changes are not saved', reply_markup=kb_start)
