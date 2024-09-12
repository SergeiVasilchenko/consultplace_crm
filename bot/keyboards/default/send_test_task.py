from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

send_test_task = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сдать задачу')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
