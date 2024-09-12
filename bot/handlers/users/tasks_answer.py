from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.config import URL_BASE
from db_responce import log_put
from filters import IsPrivate, IsTestStage
from keyboards.default import send_test_task
from loader import dp
from special_fuc import del_message, edit_message


class TestTaskState(StatesGroup):
    send_answer = State()


@dp.message_handler(IsPrivate(), IsTestStage())
async def tasks_callback(message: types.Message, state: FSMContext):
    if message.text == 'Сдать задачу':
        await message.answer(text='Отправь мне ссылку на решение')
        await TestTaskState.send_answer.set()
    else:
        await del_message(state=state, chat_id=message.from_user.id)
        await message.answer(text='Для продолжения сдайте тестовое задание и дождитесь проверки')
        data = await state.get_data()
        msg = await message.answer(text=data['test_task_text'] + data['test_task_answer'], reply_markup=send_test_task)
        await state.update_data(message_id=msg.message_id)


@dp.message_handler(IsPrivate(), IsTestStage(), state=TestTaskState.send_answer)
async def tasks_callback(message: types.Message, state: FSMContext):
    res = log_put(url=f'{URL_BASE}/testtaskscores/{message.from_user.id}/', json_={"url": message.text})
    await del_message(state=state, chat_id=message.from_user.id)
    data = await state.get_data()
    if res:
        await state.update_data(test_task_answer=f' {message.text}')
        answer = f' {message.text}'
    else:
        await message.answer(text='Произошла ошибка, попробуйте позже')
        answer = data['test_task_answer']
    msg = await message.answer(text=data['test_task_text'] + answer, reply_markup=send_test_task)
    await state.update_data(message_id=msg.message_id)
    await state.reset_state(with_data=False)


# async def tasks_callback(call: types.CallbackQuery, state: FSMContext):
#     if message.values.get('text'):
#         await TaskState.answer.set()
#         await message.answer(text='Отправьте ваш ответ в формате docx или pdf')
#     elif message.values.get('document'):
#         dow_file = await dp.bot.download_file_by_id(message.document.file_id)
#         with open(message.document.file_name, 'wb') as new_file:
#             new_file.write(dow_file.getvalue())
#         print('done')
#         await state.finish()
