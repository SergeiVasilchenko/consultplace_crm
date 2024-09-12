from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import URL_BASE
from db_responce import log_get
from filters import IsNewUser, IsPrivate, IsTestStage
from handlers.users.tasks_answer import tasks_callback
from keyboards.default import (a_kb_start, kb_start, new_kb_start,
                               send_test_task)
from loader import dp

# админ
# @rate_limit(limit=15)
# @dp.message_handler(IsPrivate(), commands=['start'], chat_id=admins_id, state="*")
# async def command_start(message: types.Message, state: FSMContext):
#     await message.answer(text=f"""Здравствуй, {message.from_user.first_name}!\n\
# Функции администратора доступны.""", reply_markup=a_kb_start)
#     await state.finish()
#     await state.reset_state()


# новый пользователь
@dp.message_handler(IsPrivate(), IsNewUser(), commands=['start'], state="*")
async def new_start(message: types.Message, state: FSMContext):
    text = '''Привет! Прежде чем мы приступим к регистрации, хотелось бы обратить твое внимание на важный момент. 
При заполнении анкеты, пожалуйста, отнесись к предоставлению информации о вашем образовании, пройденных курсах и 
профессиональном опыте максимально серьезно и честно. Подробные и точные данные помогут нам подобрать для Вас 
соответствующие проекты и  спланировать карьерную траекторию. Это поможет сделать обучение максимально эффективным 
и интересным. Благодарим за ответственность и внимание к развитию!'''
    await message.answer(text=text, reply_markup=new_kb_start)
    # video = types.InputFile('data/2408144046640.mp4')
    # photo = types.InputFile('data/tuTKhNcr5qY.jpg')
    # await message.answer_photo(photo=photo)
    # await message.answer_video(video=video)
    await state.finish()
    await state.reset_state()


@dp.message_handler(IsPrivate(), IsTestStage(), commands=['start'], state="*")
async def test_start(message: types.Message, state: FSMContext):
    await tasks_callback(message, state)


@dp.message_handler(IsPrivate(), commands=['start'], state="*")
async def old_start(message: types.Message, state: FSMContext):
    res = log_get(url=f'{URL_BASE}/detail-update/{message.from_user.username}/')
    if res:
        pass
    else:
        await message.answer(
            text='We have problems with the server, wait until we can fix everything. Apologize for the inconvenience')
    await message.answer(text=f"""Hello, {message.from_user.first_name}!\n\
I am YouStar's Assistant Bot.\n\
Part of the knowledge library is available to you now.\n\
I can also generate a response to your request.""", reply_markup=kb_start)
    await state.finish()
    await state.reset_state()
