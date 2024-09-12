from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_manage = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='Basic information',
                                                              callback_data='basic_acc_edit')
                                     ],
                                     [
                                         InlineKeyboardButton(text='Education',
                                                              callback_data='edu_acc_edit')
                                     ],
                                     [
                                         InlineKeyboardButton(text='Interests',
                                                              callback_data='int_acc_edit')
                                     ], [
                                         InlineKeyboardButton(text='Resume',
                                                              callback_data='reg_cv')
                                     ], [
                                         InlineKeyboardButton(text='Back',
                                                              callback_data='cancel_acc'),
                                         InlineKeyboardButton(text='Save',
                                                              callback_data='reg_send')
                                     ]
                                 ]
                                 )

ikb_acc_1_stage = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text='Full name',
                                                                    callback_data='reg_fio'),
                                               InlineKeyboardButton(text='Age',
                                                                    callback_data='reg_age'),
                                               InlineKeyboardButton(text='Sex',
                                                                    callback_data='reg_sex')
                                           ], [
                                               InlineKeyboardButton(text='Phone',
                                                                    callback_data='reg_phone'),
                                               InlineKeyboardButton(text='Mail',
                                                                    callback_data='reg_mail'),
                                               InlineKeyboardButton(text='Workload',
                                                                    callback_data='reg_work_time')
                                           ], [
                                               InlineKeyboardButton(text='Back', callback_data='acc_back')
                                           ]
                                       ]
                                       )

ikb_acc_2_stage = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text='Education',
                                                                    callback_data='reg_education'),
                                               InlineKeyboardButton(text='University',
                                                                    callback_data='reg_university'),
                                               InlineKeyboardButton(text='Faculty',
                                                                    callback_data='reg_faculty'),
                                               InlineKeyboardButton(text='Course',
                                                                    callback_data='reg_course')
                                           ], [
                                               InlineKeyboardButton(text='Back', callback_data='acc_back')
                                           ]
                                       ]
                                       )

ikb_acc_3_stage = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text='Edit Interests',
                                                                    callback_data='reg_interests')
                                           ], [
                                               InlineKeyboardButton(text='Edit Niches',
                                                                    callback_data='reg_nishi')
                                           ], [
                                               InlineKeyboardButton(text='Edit Goals',
                                                                    callback_data='reg_goal')
                                           ], [
                                               InlineKeyboardButton(text='Back', callback_data='acc_back')
                                           ]
                                       ]
                                       )
