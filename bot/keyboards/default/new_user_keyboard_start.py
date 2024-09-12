from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

new_kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Registration')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
