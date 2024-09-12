import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from filters import IsPrivate
from keyboards.default import kb_start
from keyboards.inline import (kb_choose_feedback, kb_feedback,
                              kb_feedback_cancel)
from loader import dp

# from data.config import review



class feedback_state(StatesGroup):
    check = State()


@dp.message_handler(IsPrivate(), text='Отзывы')
async def rev_start(message: types.Message):
    await message.answer('Здесь вы можете посмотреть или отправить отзывы', reply_markup=kb_feedback)


@dp.callback_query_handler(text='check_rev')
async def check_rev(call: types.CallbackQuery):
    await call.message.edit_text('Отзывы компаний-партнёров или бизнес-консультантов', reply_markup=kb_choose_feedback)


@dp.callback_query_handler(text='company')
async def company_rev(call: types.CallbackQuery):
    await call.message.delete()
    # for item in review['Компаний-партнёры']:
    #     await call.message.answer(item, reply_markup=kb_start)


@dp.callback_query_handler(text='cons')
async def cons_rev(call: types.CallbackQuery):
    await call.message.delete()
    # for item in review['Бизнес-консультанты']:
    #     await call.message.answer(item, reply_markup=kb_start)


@dp.callback_query_handler(text='cancel_rev')
async def cancel_rev(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Главное меню', reply_markup=kb_start)


@dp.callback_query_handler(text='send_rev')
async def send_check(call: types.CallbackQuery):
    await call.message.edit_text('Отправьте свой отзыв', reply_markup=kb_feedback_cancel)
    await feedback_state.check.set()


@dp.callback_query_handler(state=feedback_state.check, text='stop_rev')
async def stop_rev(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Отзыв не отправлен')
    await state.finish()


@dp.message_handler(state=feedback_state.check)
async def send_full(message: types.Message, state: FSMContext):
    # review['Бизнес-консультанты'].append(message.text)
    await message.answer('Спасибо за отзыв!', reply_markup=kb_start)

    # with open('review.json', 'w', encoding='utf-8') as f:
    #     json.dump(review, f, indent=4, ensure_ascii=False)

    await state.finish()
