from aiogram import types
from filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), commands=['help'], state='*')
async def command_help(message: types.Message):
    await message.answer(text='https://t.me/EVAVCmanager')