import random
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import REGION_FLAG, URL_BASE
from db_responce import log_get
from filters import IsPrivate
from keyboards.default import kb_start
from keyboards.inline import ikb_communication
from loader import dp
from special_fuc import del_message, edit_message


@dp.message_handler(IsPrivate(), text="📻Communications")
async def education_button(message: types.Message, state: FSMContext):
    msg = await message.answer(text="<b>Communication Section</b>", reply_markup=ikb_communication)
    await state.update_data(message_id=msg.message_id)


@dp.callback_query_handler(text="random_coffee")
async def rand_cof(call: types.CallbackQuery, state: FSMContext):
    res = log_get(url=f'{URL_BASE}/detail-update/{call.from_user.username}/')
    list_res = log_get(url=f'{URL_BASE}/list/')
    sum_of_stud = len(list_res) - 1
    random.seed(datetime.now())
    result = rand = random.randint(0, sum_of_stud)
    if res and list_res:
        ind_dict = \
            {
                'interest_first': res[f'interest_first_{REGION_FLAG}'],
                'interest_second': res[f'interest_second_{REGION_FLAG}'],
                'interest_third': res[f'interest_third_{REGION_FLAG}']
            }
        flag = 2
        while flag > 0:
            for j in range(sum_of_stud):
                i = (rand + j) % (sum_of_stud + 1)
                if list_res[i]['id'] == res['id']:
                    if i == rand:
                        rand += 1
                    continue
                stud_ind_dict = \
                    {
                        'interest_first': list_res[i][f'interest_first_{REGION_FLAG}'],
                        'interest_second': list_res[i][f'interest_second_{REGION_FLAG}'],
                        'interest_third': list_res[i][f'interest_third_{REGION_FLAG}']
                    }
                for inter in stud_ind_dict.keys():
                    st = list(set(stud_ind_dict[inter]) & set(ind_dict[inter]))
                    if len(st) >= flag:
                        result = i
                        flag = 0
                        break
            flag -= 1

    text = '<b>Communication Section</b>\n'
    text += f'I found an interesting companion for you: @{list_res[result]["tg_nickname"]}'
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=ikb_communication, text=text)


@dp.callback_query_handler(text='need_help')
async def command_help(call: types.CallbackQuery, state: FSMContext):
    text = '<b>Communication Section</b>\n'
    text += 'For help, you can contact: https://t.me/EVAVCmanager'
    await edit_message(state=state, chat_id=call.from_user.id, reply_markup=ikb_communication, text=text)


@dp.callback_query_handler(text='communication_back')
async def communication_back(call: types.CallbackQuery, state: FSMContext):
    await del_message(state=state, chat_id=call.from_user.id)
    await call.message.answer(text='Main menu', reply_markup=kb_start)
    await state.reset_state()
