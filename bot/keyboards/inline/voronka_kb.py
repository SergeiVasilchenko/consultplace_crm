from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

voronka_done = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Done✅',
                                                                 callback_data='voronka_done'),
                                        ]
                                    ])

reg_to_test = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Continue',
                                                                callback_data='voronka_test'),
                                       ]
                                   ])

# done_test_task_after_reg = InlineKeyboardMarkup(row_width=1,
#                                                 inline_keyboard=[
#                                                     [
#                                                         InlineKeyboardButton(text='Сдать задачу',
#                                                                              callback_data='done_test_task_after_reg'),
#                                                     ]
#                                                 ])

subscription = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='тариф 1',
                                                                 callback_data='tarif1'),
                                            InlineKeyboardButton(text='тариф 2',
                                                                 callback_data='tarif2'),
                                            InlineKeyboardButton(text='тариф 3',
                                                                 callback_data='tarif3'),
                                            InlineKeyboardButton(text='тариф 4',
                                                                 callback_data='tarif4')],
                                        # [
                                        #     InlineKeyboardButton(text='Free rate',
                                        #                          callback_data='free_tarif')
                                        # ]

                                    ])
