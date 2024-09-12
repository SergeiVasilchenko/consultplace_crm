from aiogram import types
from filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), text="‍👨‍💼💼Вакансии/стажировки")
async def education_button(message: types.Message):
    await message.answer(text="Chapter 💼‍Vacancies/internships💼")
