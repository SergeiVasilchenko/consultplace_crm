from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_communication = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(text='Random coffee',
                                                                      callback_data="random_coffee")
                                             ],
                                             [
                                                 InlineKeyboardButton(text='Question to Chat-GPT',
                                                                      callback_data="GPT_answer")
                                             ],
                                             [
                                                 InlineKeyboardButton(text='Help',
                                                                      callback_data="need_help")
                                             ],
                                             [
                                                 InlineKeyboardButton(text='Back',
                                                                      callback_data="communication_back")
                                             ]
                                         ]
                                         )
