from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_feedback = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Посмотреть отзывы',
                                                                callback_data='check_rev')
                                       ], [
                                           InlineKeyboardButton(text='Отправить отзыв',
                                                                callback_data='send_rev')
                                       ], [
                                           InlineKeyboardButton(text='Выход',
                                                                callback_data='cancel_rev')
                                       ]
                                   ]
                                   )

kb_choose_feedback = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Компаний-партнёры',
                                                                       callback_data='company')
                                              ], [
                                                  InlineKeyboardButton(text='Бизнес-консультанты',
                                                                       callback_data='cons')
                                              ], [
                                                  InlineKeyboardButton(text='Выход',
                                                                       callback_data='cancel_rev')
                                              ]
                                          ]
                                          )

kb_feedback_cancel = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [InlineKeyboardButton(text='Отмена',
                                                                    callback_data='stop_rev')]
                                          ]
                                          )
