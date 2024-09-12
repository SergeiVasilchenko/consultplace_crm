from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_reg_1_stage = InlineKeyboardMarkup(row_width=1,
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
                                               InlineKeyboardButton(text='Cancel', callback_data='reg_cancel'),
                                               InlineKeyboardButton(text='Next stage',
                                                                    callback_data='reg_next_stage_1')
                                           ]
                                       ]
                                       )

ikb_reg_2_stage = InlineKeyboardMarkup(row_width=1,
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
                                               InlineKeyboardButton(text='To the previous stage',
                                                                    callback_data='reg_prev_stage_2'),
                                               InlineKeyboardButton(text='To the next stage',
                                                                    callback_data='reg_next_stage_2')
                                           ], [
                                               InlineKeyboardButton(text='Cancel', callback_data='reg_cancel')
                                           ]
                                       ]
                                       )

ikb_reg_2_stage_education = InlineKeyboardMarkup(row_width=1,
                                                 inline_keyboard=[
                                                     [
                                                         InlineKeyboardButton(text='Education',
                                                                              callback_data='reg_education')
                                                     ], [
                                                         InlineKeyboardButton(text='To the previous stage',
                                                                              callback_data='reg_prev_stage_2'),
                                                         InlineKeyboardButton(text='To the next stage',
                                                                              callback_data='reg_next_stage_2')
                                                     ], [
                                                         InlineKeyboardButton(text='Cancel', callback_data='reg_cancel')
                                                     ]
                                                 ]
                                                 )

ikb_reg_3_stage = InlineKeyboardMarkup(row_width=1,
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
                                               InlineKeyboardButton(text='To the previous stage',
                                                                    callback_data='reg_prev_stage_3'),
                                               InlineKeyboardButton(text='Complete registration',
                                                                    callback_data='reg_send')
                                           ], [
                                               InlineKeyboardButton(text='Cancel', callback_data='reg_cancel')
                                           ]
                                       ]
                                       )

ikb_reg_start = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Добавить/Редактировать ФИО',
                                                                  callback_data='reg_fio')
                                         ], [
                                             InlineKeyboardButton(text='Добавить/Редактировать почту',
                                                                  callback_data='reg_mail')
                                         ], [
                                             InlineKeyboardButton(text='Сохранить', callback_data='reg_send'),
                                             InlineKeyboardButton(text='Отмена', callback_data='reg_cancel')
                                         ]
                                     ]
                                     )

ikb_sex = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text='Male',
                                                            callback_data='male'),
                                       InlineKeyboardButton(text='Female',
                                                            callback_data='female')
                                   ]
                               ]
                               )

ikb_cancel = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Cancel',
                                                               callback_data='reg_cancel_true'),
                                          InlineKeyboardButton(text='To stay',
                                                               callback_data='reg_stay')
                                      ]
                                  ]
                                  )

ikb_to_voronka = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Continue',
                                                                   callback_data='reg_to_voronka')
                                          ]
                                      ]
                                      )
