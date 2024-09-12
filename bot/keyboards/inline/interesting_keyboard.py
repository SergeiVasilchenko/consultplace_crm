from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

int_kb_1 = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Предпринимательство',
                                                             callback_data='int_1_1')
                                    ], [
                                        InlineKeyboardButton(text='Инновационное предпринимательство',
                                                             callback_data='int_1_2')
                                    ], [
                                        InlineKeyboardButton(text='Венчурные инвестиции',
                                                             callback_data='int_1_3')
                                    ], [
                                        InlineKeyboardButton(text='Классические инвестиции',
                                                             callback_data='int_1_4')
                                    ], [
                                        InlineKeyboardButton(text='Стратегический консалтинг',
                                                             callback_data='int_1_5')
                                    ], [
                                        InlineKeyboardButton(text='Инвест. банкинг',
                                                             callback_data='int_1_6')
                                    ], [
                                        InlineKeyboardButton(text='M&A, PE',
                                                             callback_data='int_1_7')
                                    ], [
                                        InlineKeyboardButton(text='Финансы',
                                                             callback_data='int_1_8')
                                    ], [
                                        InlineKeyboardButton(text='Назад', callback_data='reg_send'),
                                        InlineKeyboardButton(text='Сохранить', callback_data='reg_cancel')
                                    ]
                                ]
                                )
