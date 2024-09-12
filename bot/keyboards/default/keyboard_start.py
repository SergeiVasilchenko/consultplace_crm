from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

#
# kb_start = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='Библиотека')
#         ],
#         [
#             KeyboardButton(text='Личный кабинет')
#         ],
#         [
#             KeyboardButton(text='Отзывы')
#         ]
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )

# новый вариант меню от Екатерины
kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Personal account')
        ],
        [
            KeyboardButton(text='🎓Training')
        ],
        [
            KeyboardButton(text='📻Communications')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
