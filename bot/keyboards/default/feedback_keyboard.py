from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_feedback = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Посмотреть отзывы')
        ],
        [
            KeyboardButton(text='Отправить отзыв')
        ]
    ],
    resize_keyboard=True
)

kb_choose_feedback = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Компаний-партнёры')
        ],
        [
            KeyboardButton(text='Бизнес-консультанты')
        ]
    ],
    resize_keyboard=True
)

kb_feedback_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)