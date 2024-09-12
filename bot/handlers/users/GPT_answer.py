import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from filters import IsPrivate
from loader import dp, openai

# import g4f

TPM_35_TURBO = 40000
RPM_35_TURBO = 3
RPD_35_TURBO = 200

CONTEX_MSG_LEN = 4


class GPTState(StatesGroup):
    gpt = State()


async def chat_gpt(text: str, state: FSMContext):
    data = await state.get_data()
    if not data.get('chat_response'):
        await state.update_data(chat_response=[{"role": "user", "content": text}])
        messages = [{"role": "user", "content": text}]
    else:
        async with state.proxy() as data:
            data['chat_response'] += [{"role": "user", "content": text}]
            data['chat_response'] = data['chat_response'][2:] if len(data['chat_response']) > CONTEX_MSG_LEN else \
                data['chat_response']
            messages = data['chat_response']

    try:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        async with state.proxy() as data:
            data['chat_response'] += [{"role": "assistant", "content": completion.choices[0].message.content}]
    except Exception as ex:
        logging.error(ex)
        return False

    return completion.choices[0].message.content
    #
    # await state.reset_state()
    # await state.finish()


async def chat_g4f(text: str, state: FSMContext):
    # data = await state.get_data()
    # if not data.get('chat_response'):
    #     await state.update_data(chat_response=[{"role": "user", "content": text}])
    #     messages = [{"role": "user", "content": text}]
    # else:
    #     async with state.proxy() as data:
    #         data['chat_response'] += [{"role": "user", "content": text}]
    #         data['chat_response'] = data['chat_response'][2:] if len(data['chat_response']) > CONTEX_MSG_LEN else \
    #             data['chat_response']
    #         messages = data['chat_response']
    #
    # print(messages)

    # response = await g4f.ChatCompletion.create_async(
    #     model=g4f.models.default,
    #     messages=[{"role": "user", "content": text}],
    #     provider=g4f.Provider.GeekGpt,
    # )
    # print(response)
    # chat_gpt_response = response
    #
    # return chat_gpt_response
    pass


@dp.callback_query_handler(text="GPT_answer")
async def gpt_help(call: types.callback_query):
    text = '''GPT assistant is ready to help you
Just send your question with a message
To exit the chat with GPT use /start'''
    await call.message.answer(text=text)
    await GPTState.gpt.set()


@dp.message_handler(text="/restart")
async def gpt_help(message: types.Message, state: FSMContext):
    await state.update_data(chat_response=[])
    await message.answer(text="Начат новый диалог")


@dp.message_handler(IsPrivate(), state=GPTState.gpt)
async def gpt_answer(message: types.Message, state: FSMContext):
    # mes = await message.answer(text='ㅤ\nСообщение получено!\nㅤ')
    # await chat_gpt(message.text, message_id=mes.message_id, chat_id=mes.chat.id)
    # await dp.bot.edit_message_text(message_id=mes.message_id, chat_id=mes.chat.id, text='ㅤ\nГенерация ответа⏳\nㅤ')
    answer = await chat_gpt(text=f'{message.text}', state=state)
    if answer:
        await message.answer(text=f'{answer}\n\nTo start a new conversation, enter /restart')
    else:
        await message.answer(text=f'It seems we have something broken, sorry for the inconvenience')
    # task_gpt_answer = asyncio.create_task(chat_gpt(message.text, message_id=mes.message_id, chat_id=mes.chat.id))
    # task_wait_message = asyncio.create_task(
    #     dp.bot.edit_message_text(message_id=mes.message_id, chat_id=mes.chat.id, text='ㅤ\nГенерация ответа⏳\nㅤ'))
    # await task_gpt_answer
    # await task_wait_message



