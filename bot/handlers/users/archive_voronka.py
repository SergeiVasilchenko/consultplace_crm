# import logging
#
# import requests
# from aiogram import types
# from aiogram.types import InputMediaVideo, InputMediaPhoto, ContentType
# from data import config
#
# from db_responce import log_get
# from filters import IsPrivate
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.dispatcher import FSMContext
# from .tests import tests
# from data.config import PAYMENT_TOKEN
# from keyboards.default import kb_start
# from keyboards.inline import voronka_done, subscription
# from loader import dp
#
#
# class VoronkaState(StatesGroup):
#     test_task = State()
#     stage1 = State()
#     stage2 = State()
#     stage3 = State()
#     stage4 = State()
#
#
# # TODO stage for voronka
# @dp.callback_query_handler(state=VoronkaState.stage1)
# async def stage1(call: types.CallbackQuery, state: FSMContext):
#     # получаем урл из црм
#     text = 'Complete the test task so that we can understand your level\n https://docs.google.com/document/d/1XFu9qvZjnqGgqoeP0RRwYFXymsUK_nrKOC_pmwo7o7k/edit'
#     # video_1 = types.InputFile('data/2408144046640.mp4')
#     # photo = types.InputFile('data/tuTKhNcr5qY.jpg')
#     # await call.message.answer_photo(photo='https://consultplace.sytes.net/media/Files/logo_login.jpg')
#     # await call.message.answer_video(video='https://samplelib.com/lib/preview/mp4/sample-5s.mp4', caption=text,
#     #                                 reply_markup=voronka_done)
#
#     ikb_acc_2_stage = InlineKeyboardMarkup(inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Education',
#                                  callback_data='reg_education'),
#             InlineKeyboardButton(text='University',
#                                  callback_data='reg_university'),
#             InlineKeyboardButton(text='Faculty',
#                                  callback_data='reg_faculty'),
#             InlineKeyboardButton(text='Course',
#                                  callback_data='reg_course')
#         ], [
#             InlineKeyboardButton(text='Back', callback_data='acc_back')
#         ]
#     ]
#     )
#
#     await call.message.answer(text=text, reply_markup=kb_start)
#     await state.reset_state(False)
#     # await VoronkaState.test_task.set()
#
#
# # @dp.callback_query_handler(state=VoronkaState.stage1)
# # async def stage2(call: types.CallbackQuery, state: FSMContext):
# #     message_id = await state.get_data()
# #     message_id = message_id['message_id']
# #     if message_id:
# #         try:
# #             await dp.bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
# #         except Exception as ex:
# #             logging.error(ex)
# #         await state.update_data(message_id=0)
# #     url = ''  # откуда брать тесты из црм
# #     test_resp = await tests(call, state, url)
# #     await VoronkaState.stage1.set()
# #     if test_resp:
# #         text = ('Now you can familiarize yourself with the tariffs and choose the most convenient one for yourself.\n'
# #                 'level 1 - blah blah blah 50r/year\n'
# #                 'level 2 - blah blah blah 500r/year\n'
# #                 'level 3 - blah blah 5000r/year\n'
# #                 'level 4 - blah blah blah 50000r/year\n'
# #                 'free use - blah blah blah')
# #         await call.message.answer(text=text, reply_markup=subscription)
# #         await VoronkaState.stage2.set()
#
#
# # @dp.callback_query_handler(text=['tarif1', 'tarif2', 'tarif3', 'tarif4'], state=VoronkaState.stage2)
# # async def payment(call: types.CallbackQuery):
# #     # if PAYMENT_TOKEN.split(':')[1] == 'TEST':
# #     #     await call.message.answer("Тестовый платеж!!!")
# #
# #     price = 0
# #
# #     if call.data[-1] == '1':
# #         price = types.LabeledPrice(label="Tier 1 subscription", amount=100 * 100)
# #     elif call.data[-1] == '2':
# #         price = types.LabeledPrice(label="Tier 2 subscription", amount=200 * 100)
# #     elif call.data[-1] == '3':
# #         price = types.LabeledPrice(label="Tier 3 subscription", amount=300 * 100)
# #     elif call.data[-1] == '4':
# #         price = types.LabeledPrice(label="Tier 4 subscription", amount=400 * 100)
# #
# #     if price != 0:
# #         await dp.bot.send_invoice(call.message.chat.id,
# #                                   title="Subscription",
# #                                   description="This is a subscription to a chatbot",
# #                                   provider_token=config.PAYMENT_TOKEN,
# #                                   currency="RUB",
# #                                   prices=[price],
# #                                   payload="HUYNIA",
# #                                   photo_url="http://194.67.86.225/static/logo_EVAVC.jpg"
# #                                             "-3e0070aa19a7fe36e802253048411a38f14a79f8-s1100-c50.jpg"
# #                                   )
# #         await VoronkaState.stage3.set()
#
#
# @dp.callback_query_handler(text='free_tarif', state=VoronkaState.stage2)
# async def free_tarif(call: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await call.message.answer(text="Подписка оформлена", reply_markup=kb_start)
#
#
# @dp.pre_checkout_query_handler(lambda query: True, state='*')
# async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
#     text = "Aliens tried to steal your card's CVV," \
#            " but we successfully protected your credentials," \
#            " try to pay again in a few minutes, we need a small rest."
#     await dp.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True, error_message=text)
#
#
# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')
# async def successful_payment(message: types.Message, state: FSMContext):
#     await state.finish()
#     # print("SUCCESSFUL PAYMENT:")
#     payment_info = message.successful_payment.to_python()
#     # for k, v in payment_info.items():
#     #     pass
#     #     # print(f"{k} = {v}")
#
#     await dp.bot.send_message(message.chat.id, f"Subscription is issued", reply_markup=kb_start)
#
# #  1111 1111 1111 1026
# #  12 25 000
# #  content_types=[ContentType.SUCCESSFUL_PAYMENT]
