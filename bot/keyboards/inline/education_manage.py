from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_education = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='My tasks',
                                                                  callback_data="edu_student_tasks")
                                         ],
                                         [
                                             InlineKeyboardButton(text='📚Knowledge Library📚',
                                                                  callback_data="library")
                                         ],
                                         [
                                             InlineKeyboardButton(text='🛣🗺Road map',
                                                                  callback_data="road_map")
                                         ],
                                         [
                                             InlineKeyboardButton(text='Video seminars',
                                                                  callback_data='2132541254')
                                         ],
                                         [
                                             InlineKeyboardButton(text='Back',
                                                                  callback_data="education_back")
                                         ],
                                     ]
                                     )

# ikb_student_project = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Submit a task',
#                              callback_data="edu_submit_a_task")
#     ], [
#         InlineKeyboardButton(text='Back',
#                              callback_data="edu_student_tasks_back")
#     ]
# ]
# )

ikb_road_map = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Back',
                             callback_data="edu_road_map_back")
    ]
]
)
