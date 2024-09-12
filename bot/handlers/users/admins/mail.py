import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from data.config import admins_id
from keyboards.default import a_kb_start
from keyboards.inline import ikb_mail
from loader import dp


class MailState(StatesGroup):
    text = State()
    picture = State()
    check = State()


# запуск рассылки
@dp.message_handler(text='Рассылка', chat_id=admins_id)
async def command_help(message: types.Message):
    await MailState.text.set()
    await message.answer(
        'Введите текст рассылки:',
        reply_markup=ReplyKeyboardRemove()
    )


# получение первичного текста рассылки
@dp.message_handler(state=MailState.text)
async def mail_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await MailState.check.set()
    if 'picture' in data:
        await message.answer_photo(
            photo=data['picture'],
            caption=data['text'],
            reply_markup=ikb_mail
        )
    else:
        await message.answer(text=message.text, reply_markup=ikb_mail)


# получение картинки
@dp.callback_query_handler(text='mail_picture', state=MailState.check)
async def mail_picture(message: types.Message):
    await MailState.picture.set()
    await dp.bot.send_message(message.from_user.id, 'Отправьте мне картинку')


@dp.callback_query_handler(text='mail_text', state=MailState.check)
async def mail_picture(message: types.Message):
    await MailState.text.set()
    await dp.bot.send_message(
        message.from_user.id,
        'Отправьте редактированный текст:'
    )


@dp.message_handler(lambda message: not message.photo, state=MailState.picture)
async def is_image(message: types.Message):
    await message.answer(text="Это не картинка!")


# получение картинки
@dp.message_handler(
    state=MailState.picture,
    content_types=types.ContentTypes.PHOTO
)
async def mail_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['picture'] = message.photo[0].file_id
    await MailState.check.set()
    if 'text' in data:
        await message.answer_photo(
            photo=data['picture'],
            caption=data['text'],
            reply_markup=ikb_mail
        )
    else:
        await message.answer_photo(
            photo=data['picture'],
            reply_markup=ikb_mail
        )


# отправка тотально - железно
@dp.callback_query_handler(text='send', state=MailState.check)
async def mail_text(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['check'] = 1
    # тут отправка всем
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    if 'picture' in data:
        for user in users:
            await dp.bot.send_photo(chat_id=int(user), photo=data['picture'],
                                    caption=data['text'],
                                    reply_markup=a_kb_start)
    else:
        for user in users:
            await dp.bot.send_message(
                chat_id=int(user),
                text=data['text'],
                reply_markup=a_kb_start
            )
    await call.message.answer('Готово')
    await state.finish()


@dp.callback_query_handler(text='cancel', state=MailState.check)
async def mail_check(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено', reply_markup=a_kb_start)
    await state.finish()
