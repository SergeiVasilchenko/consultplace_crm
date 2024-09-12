from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

a_kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Библиотека'),
            KeyboardButton(text='Рассылка')
        ]
    ],
    resize_keyboard=True
)
