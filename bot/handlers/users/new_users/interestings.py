# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.types import CallbackQuery
#
# from loader import dp
# from keyboards.default import kb_start, new_kb_start
# from keyboards.inline import ikb_reg
#
# from filters import IsNewUser, IsPrivate
#
# from handlers.users.new_users.registration import RegState
#
#
# @dp.callback_query_handler(text='reg_interest', state=RegState.check)
# async def reg_mail_button(call: types.CallbackQuery):
#     await call.message.edit_text('Выбери интерес', reply_markup=int_kb_1)
