import logging

import aiogram.utils.exceptions
from loader import dp


async def edit_message(state, chat_id, text, reply_markup):
    data = await state.get_data()
    # if data['message_txt'] == text:
    #     print('228')
    #     return
    try:
        msg = await dp.bot.edit_message_text(text=text, chat_id=chat_id, message_id=data['message_id'],
                                             reply_markup=reply_markup)
    except aiogram.utils.exceptions.MessageIdInvalid as ex:
        msg = await dp.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        logging.error(ex)

    await state.update_data(message_id=msg.message_id)


async def del_message(state, chat_id, list_mode=False):
    data = await state.get_data()
    if list_mode:
        for msg_id in data['message_ids']:
            try:
                await dp.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as ex:
                logging.error(ex)
    else:
        try:
            await dp.bot.delete_message(chat_id=chat_id, message_id=data['message_id'])
        except Exception as ex:
            logging.error(ex)
