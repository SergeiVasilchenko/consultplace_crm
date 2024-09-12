# import logging

from aiogram import types
from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup())
async def new_chat(message: types.Message):
    print(message)
