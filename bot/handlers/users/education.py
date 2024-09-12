from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import URL_BASE
from db_responce import log_get, log_post
from filters import IsPrivate
from keyboards.default import kb_start
from keyboards.inline import ikb_education, ikb_road_map
from loader import dp
from special_fuc import del_message, edit_message

education_text = '''<b>🎓Training</b>
Here you can see the statuses for your current projects as well as improve your knowledge in the library!'''


class EduState(StatesGroup):
    tasks = State()
    send_task = State()


@dp.message_handler(IsPrivate(), text="🎓Training")
async def education_button(message: types.Message, state: FSMContext):
    msg = await message.answer(text=education_text, reply_markup=ikb_education)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query_handler(text="education_back")
async def edu_to_start(call: types.CallbackQuery, state: FSMContext):
    text = 'Main screen'
    await call.message.answer(text=text, reply_markup=kb_start)
    await del_message(state=state, chat_id=call.from_user.id)
    await state.reset_state()


def gen_data(call):
    student_resp = log_get(url=f'{URL_BASE}/detail-update/{call.from_user.username}/')
    student_id = student_resp['id'] if student_resp else 0
    text = "You don't have any tasks yet"
    tasks_name_id = {}

    project_text_list = []
    project_resp = log_get(url=f'{URL_BASE}/projects/')
    if project_resp and student_id:
        projects_id = {}
        for project in project_resp:
            if student_id in project['students']:
                projects_id[project['id']] = project['name']

        for item in projects_id.values():
            task_resp = log_get(url=f'{URL_BASE}/taskstudents/?project__name={item}')
            if not task_resp:
                continue
            # task_groups_resp = log_get(
            #     url=f'{URL_BASE}/taskgroups/?project__name={item}')
            # task_group_description = task_groups_resp[0]['description'] if task_groups_resp else ''
            for task in task_resp:
                if task['assigned_student'] == student_id:
                    tasks_name_id[task['description']] = task['id']
                    text = f"Project: {item}\nStart date: {task['start_date']}\nEnd date: {task['end_date']}\nYour task is: {task['description']}\n\n"
                    project_text_list.append({'text': text, 'id': task['id']})

        return project_text_list


def gen_kb(page, data_len):
    kb_base = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Submit a task',
                                                                          callback_data="edu_submit_a_task")]])
    kb_add = []
    if page > 0:
        kb_add.append(InlineKeyboardButton(text='previous', callback_data="edu_student_previous_task"))
    if page < data_len - 1:
        kb_add.append(InlineKeyboardButton(text='next', callback_data="edu_student_next_task"))

    kb_base.add(*kb_add)
    kb_base.add(InlineKeyboardButton(text='Back', callback_data="edu_student_tasks_back"))

    return kb_base


@dp.callback_query_handler(text=["edu_student_tasks", "edu_submit_a_task_back"], state='*')
async def edu_student_tasks(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'edu_student_tasks':
        tasks_data = gen_data(call)
        page = 0
        kb = gen_kb(page, len(tasks_data))
        if tasks_data == []:
            tasks_data = [{'text': "You don't have any tasks yet"}]
            kb = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Back', callback_data="edu_student_tasks_back")]])
        await state.update_data(tasks_page=0)
    else:
        data = await state.get_data()
        tasks_data = data['tasks_text']
        page = data['tasks_page']
        kb = gen_kb(page, len(tasks_data))

    text = '<b>My Tasks</b>\n\n' + tasks_data[page]['text']

    # ans_resp = log_get(url=f'{URL_BASE}/projects/')
    await state.update_data(tasks_text=tasks_data)
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=kb, text=text)
    await state.reset_state(False)


@dp.callback_query_handler(text=['edu_student_next_task', 'edu_student_previous_task'])
async def next_task(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks_data = data['tasks_text']
    page = data['tasks_page']

    if call.data == 'edu_student_next_task':
        page += 1
    if call.data == 'edu_student_previous_task':
        page -= 1

    text = '<b>My Tasks</b>\n\n' + tasks_data[page]['text']
    await state.update_data(tasks_page=page)
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=gen_kb(page, len(tasks_data)), text=text)
    await state.reset_state(False)


@dp.callback_query_handler(text='edu_submit_a_task')
async def edu_student_send_tasks(call: types.CallbackQuery, state: FSMContext):
    text = 'Send the solution file or a link to the file'
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Back', callback_data="edu_submit_a_task_back")]])
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=kb, text=text)
    await EduState.send_task.set()


@dp.message_handler(state=EduState.send_task)
async def edu_student_tasks(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tasks_data = data['tasks_text']
    page = data['tasks_page']

    task_id = tasks_data[page]['id']
    data = {
        "url": message.text,
        "answer": task_id,
        "user": 1
    }
    resp = log_post(url=f'{URL_BASE}/answersstudents/', json_=data)
    if resp:
        text = 'The answer is saved'
    else:
        text = 'Some kind of error has occurred please try again later'
    await message.answer(text=text)
    await del_message(state=state, chat_id=message.from_user.id)
    text = '<b>My Tasks</b>\n\n' + tasks_data[page]['text']
    msg = await message.answer(reply_markup=gen_kb(page, len(tasks_data)), text=text)
    await state.reset_state(False)
    await state.update_data(message_id=msg.message_id)


@dp.message_handler(state=EduState.send_task, content_types=types.ContentTypes.DOCUMENT)
async def reg_cv_button(message: types.ContentTypes.DOCUMENT, state: FSMContext):
    data = await state.get_data()
    tasks_data = data['tasks_text']
    page = data['tasks_page']

    file = message.document  # получение дока
    file_name = file['file_name']

    file_info = await dp.bot.get_file(file.file_id)
    file = await dp.bot.download_file(file_info.file_path)  # преобразование в битовую последовательность

    file.name = file_name

    task_id = tasks_data[page]['id']
    data = {
        "answer": task_id,
        "user": 1,
    }
    file = {'file': file}
    resp = log_post(url=f'{URL_BASE}/answersstudents/', data=data, files=file)
    if resp:
        text = 'The answer is saved'
    else:
        text = 'Some kind of error has occurred please try again later'
    await message.answer(text=text)
    await del_message(state=state, chat_id=message.from_user.id)
    text = '<b>My Tasks</b>\n\n' + tasks_data[page]['text']
    msg = await message.answer(reply_markup=gen_kb(page, len(tasks_data)), text=text)
    await state.reset_state(False)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query_handler(text="edu_student_tasks_back")
async def edu_student_tasks(call: types.CallbackQuery, state: FSMContext):
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=ikb_education, text=education_text)


@dp.callback_query_handler(text="road_map")
async def edu_student_tasks(call: types.CallbackQuery, state: FSMContext):
    photo = types.InputFile('data/map.jpg')
    text = 'The roadmap of our course'
    await del_message(state=state, chat_id=call.from_user.id)
    msg = await call.message.answer_photo(photo=photo, caption=text, reply_markup=ikb_road_map)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query_handler(text="edu_road_map_back")
async def edu_student_tasks(call: types.CallbackQuery, state: FSMContext):
    await del_message(state=state, chat_id=call.from_user.id)
    msg = await call.message.answer(text=education_text, reply_markup=ikb_education)
    await state.update_data(message_id=msg.message_id)
