from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_inter = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='Edit Interests',
                                                              callback_data='interests')
                                     ], [
                                         InlineKeyboardButton(text='Edit Niches',
                                                              callback_data='nishi')
                                     ], [
                                         InlineKeyboardButton(text='Edit Goals',
                                                              callback_data='goals')
                                     ], [
                                         InlineKeyboardButton(text='Back',
                                                              callback_data='account_edit')
                                     ]
                                 ]
                                 )

ikb_inter_1 = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Edit Interests',
                                                                callback_data='interests')
                                       ], [
                                           InlineKeyboardButton(text='Edit Niches',
                                                                callback_data='nishi')
                                       ], [
                                           InlineKeyboardButton(text='Edit Goals',
                                                                callback_data='goals')
                                       ], [
                                           InlineKeyboardButton(text='Back',
                                                                callback_data='account_edit_1')
                                       ]
                                   ]
                                   )
