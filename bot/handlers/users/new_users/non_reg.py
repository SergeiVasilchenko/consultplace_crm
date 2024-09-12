from aiogram import types
from filters import IsNewUser, IsPrivate
from keyboards.default import new_kb_start
from loader import dp


# отвечат на любые запросы незарегистрированным пользователям
@dp.message_handler(IsPrivate(), IsNewUser())
async def command_error(message: types.Message):
    await message.answer(
        text='You are not registered yet.',
        reply_markup=new_kb_start
    )
