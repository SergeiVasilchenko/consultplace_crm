from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_mail = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Добавить/Редактировать текст',
                                                               callback_data='mail_text')
                                      ], [
                                          InlineKeyboardButton(text='Добавить/Редактировать изображение',
                                                               callback_data='mail_picture')
                                      ], [
                                          InlineKeyboardButton(text='Отправить', callback_data='send'),
                                          InlineKeyboardButton(text='Отмена', callback_data='cancel')
                                      ]
                                  ]
                                )
