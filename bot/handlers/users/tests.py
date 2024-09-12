# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# from filters import IsPrivate
# from loader import dp
#
#
# class TestState(StatesGroup):
#     test = State()
#
#
# async def tests(message, state: FSMContext, url='', msg_id=None):
#     test_data = {'Вопрос 1?': [['12', '23', '34'], 1], 'Вопрос2?11': [['1', '3', '4'], 1]}
#
#     async with state.proxy() as data:
#         if data.get('page') is not None:
#             data['answer_counter'] += 1 if (int(message.data[-1]) == data['answers'][data['page']][1]) else 0
#             data['page'] += 1
#         else:
#             await TestState.test.set()
#             data['page'] = 0
#             data['question'] = list(test_data.keys())
#             data['answers'] = list(test_data.values())
#             data['answer_counter'] = 0
#             data['msg_id'] = 0 if msg_id else msg_id
#
#         page = data['page']
#         answer_counter = data["answer_counter"]
#         msg_id = data['msg_id']
#
#     if page >= len(test_data):
#         text = f'Тест закончен с результатом {answer_counter} из {len(test_data)}'
#         await dp.bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
#                                        text=text)
#         await state.finish()
#         await state.reset_state()
#         return 1
#
#     question = data['question'][page]
#     answers = data['answers'][page][0]
#
#     question_text = f'<b>Вопрос {page + 1} из {len(test_data)}</b>\n{question}'
#     test_kb = InlineKeyboardMarkup()
#     buttons = []
#
#     for i, item in enumerate(answers):
#         i += 1
#         question_text += f'\n{i}. {item}'
#         buttons += [InlineKeyboardButton(text=i, callback_data=f'test_button_{i}')]
#
#     test_kb.add(*buttons)
#
#     if page == 0:
#         if type(message) == types.Message:
#             msg = await message.answer(text=question_text, reply_markup=test_kb)
#         else:
#             msg = await message.message.answer(text=question_text, reply_markup=test_kb)
#         await state.update_data(msg_id=msg.message_id)
#     else:
#         await dp.bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
#                                        text=question_text, reply_markup=test_kb)
#
#     return 0
#
#
# @dp.message_handler(IsPrivate(), text='Тесты')
# @dp.callback_query_handler(state=TestState.test)
# async def test(message, state: FSMContext):
#     await tests(message, state)
