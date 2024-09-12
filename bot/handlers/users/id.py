from aiogram import types
from loader import dp


@dp.message_handler(commands=['id'])
async def command_error(message: types.Message):
    await message.answer(f'You ID:\n{message.from_user.id}')
