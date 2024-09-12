from aiogram import types
from filters import IsPrivate
from keyboards.default import kb_start
from loader import dp


@dp.message_handler(IsPrivate())
async def command_error(message: types.Message):
    await message.answer(
        '''Now the bot's functionality is very limited, but very soon we will launch the full version! Currently
, only registration and the communications section are available.''',
        reply_markup=kb_start)
