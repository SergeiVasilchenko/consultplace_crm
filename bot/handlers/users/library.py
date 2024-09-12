from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import URL_BASE
from db_responce import log_get
from keyboards.inline import ikb_education
from loader import dp
from special_fuc import del_message, edit_message

from .education import education_text

# playlist_bank = ['pl1', 'pl2', 'pl3', 'pl4', 'pl5', 'pl6', 'pl7', 'pl8', 'pl1', 'pl2', 'pl3', 'pl4', 'pl5', 'pl6',
#                  'pl7', 'pl8', 'pl1', 'pl2', 'pl3', 'pl4', 'pl5', 'pl6', 'pl7', 'pl8']

DATA_ON_ONE_PAGE = 5
buttons = [f'lb_{i + 1}' for i in range(DATA_ON_ONE_PAGE)]


async def text_and_kb_generation(data, start_page=0):
    last_page = len(data) // DATA_ON_ONE_PAGE
    if len(data) % DATA_ON_ONE_PAGE:
        last_page += 1
    kb_library = InlineKeyboardMarkup(row_width=5)
    buttons = []
    message_text = f'Page {start_page + 1} of {last_page} is shown\n'
    for i in range(start_page * DATA_ON_ONE_PAGE, min(start_page * DATA_ON_ONE_PAGE + DATA_ON_ONE_PAGE, len(data))):
        message_text += f'{i - start_page * DATA_ON_ONE_PAGE + 1}. {data[i]}\n'
        buttons += [InlineKeyboardButton(text=f'{i + 1 - start_page * DATA_ON_ONE_PAGE}',
                                         callback_data=f'lb_{i + 1 - start_page * DATA_ON_ONE_PAGE}')]
    kb_library.add(*buttons)
    if last_page != 1:
        if (start_page + 1) == last_page:
            buttons = [
                InlineKeyboardButton(text=f'page 1«', callback_data='first_page_pl'),
                InlineKeyboardButton(text='prev.<', callback_data='previously_pl')
            ]
        elif start_page == 0:
            buttons = [
                InlineKeyboardButton(text='next>', callback_data='next_pl'),
                InlineKeyboardButton(text=f'page {last_page}»', callback_data='last_page_pl')
            ]
        else:
            buttons = [
                InlineKeyboardButton(text=f'page 1«', callback_data='first_page_pl'),
                InlineKeyboardButton(text='prev.<', callback_data='previously_pl'),
                InlineKeyboardButton(text='next>', callback_data='next_pl'),
                InlineKeyboardButton(text=f'page {last_page}»', callback_data='last_page_pl')
            ]

        kb_library.add(*buttons)
    kb_library.add(InlineKeyboardButton(text=f'Назад', callback_data='lib_cancel'))
    return message_text, kb_library


@dp.callback_query_handler(text=['library', 'library_back'])
async def library_start(call: types.callback_query, state: FSMContext):
    student_status = log_get(url=f'{URL_BASE}/detail-update/{call.from_user.username}/')['education_status']
    if student_status in ['Base', 'Optimal']:
        url = f'{URL_BASE}/dataknowledgefree/'
    else:
        url = f'{URL_BASE}/dataknowledge/'
    res = log_get(url=url)
    playlist_bank = [item['chapter']['name'] for item in res]
    await state.update_data(res=res)
    # сохранение страница (наверное)
    async with state.proxy() as data:
        if 'pl_page_flag' not in data:
            data['pl_page_flag'] = 0

    text, kb = await text_and_kb_generation(playlist_bank, data['pl_page_flag'])
    message_text = 'Denis`s video "Ask VC" is available in our library\n' \
                   'Select the playlist you are interested in:\n'
    message_text += text

    if call.data == 'library_back':
        await edit_message(state=state, chat_id=call.from_user.id, reply_markup=kb, text=message_text)
        await del_message(state=state, chat_id=call.from_user.id, list_mode=True)
    else:
        await edit_message(state=state, chat_id=call.from_user.id, reply_markup=kb, text=message_text)

    # async with state.proxy() as data:
    #     if 'last_library_id' not in data:
    #         data['last_library_id'] = msg.message_id
    #     else:
    #         await dp.bot.delete_message(msg.chat.id, data['last_library_id'])
    #         data['last_library_id'] = msg.message_id


@dp.callback_query_handler(text=['next_pl', 'previously_pl', 'first_page_pl', 'last_page_pl'])
async def library_choose_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    playlist_bank = [item['chapter']['name'] for item in data['res']]
    print(playlist_bank)
    last_page = len(playlist_bank) // DATA_ON_ONE_PAGE

    async with state.proxy() as data:
        if 'pl_page_flag' not in data:
            pl_page_flag = 0
        else:
            pl_page_flag = data['pl_page_flag']

    if call['data'] == 'next_pl':
        if pl_page_flag < last_page:
            pl_page_flag += 1
    if call['data'] == 'previously_pl':
        if pl_page_flag > 0:
            pl_page_flag -= 1
    if call['data'] == 'first_page_pl':
        pl_page_flag = 0
    if call['data'] == 'last_page_pl':
        pl_page_flag = last_page

    async with state.proxy() as data:
        data['pl_page_flag'] = pl_page_flag

    text, kb = await text_and_kb_generation(playlist_bank, pl_page_flag)

    message_text = 'Denis`s video "Ask VC" is available in our library\n' \
                   'Select the playlist you are interested in:\n'
    message_text += text

    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=kb, text=text)


@dp.callback_query_handler(text=buttons)
async def library_choose_pl(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    but_num = call.data[-1]
    pl_num = data['pl_page_flag'] * DATA_ON_ONE_PAGE + int(but_num) - 1
    # file_url = data['res'][0]['files'][0]['file']
    res = data['res'][pl_num]
    text = f'<b>{res["chapter"]["name"]}</b>\n{res["under_section"]["name"]}'
    if res['video_url']:
        text += '\nВидео материалы ' + res[f'video_url']
    if res['url']:
        text += '\nПолезные ссылки ' + res[f'url']

    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(InlineKeyboardButton(text='back', callback_data='library_back'))

    await edit_message(state=state, chat_id=call.message.chat.id, text=text, reply_markup=reply_markup)

    if data['res'][0]['files']:
        media = types.MediaGroup()
        for item in data['res'][pl_num]['files']:
            media.attach_document(item['file'])
        msgs = await call.message.answer_media_group(media=media)
        await state.update_data(message_ids=[msg.message_id for msg in msgs])


@dp.callback_query_handler(text='lib_cancel')
async def check_rev(call: types.CallbackQuery, state: FSMContext):
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=ikb_education, text=education_text)


