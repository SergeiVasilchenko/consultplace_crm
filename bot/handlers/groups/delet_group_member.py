from aiogram import types
from filters import IsGroup
from loader import bot, dp


@dp.message_handler(
    IsGroup(),
    content_types=types.ContentTypes.LEFT_CHAT_MEMBER
)
async def left_chat_member(message: types.Message):
    # bot_onj = await bot.get_me()
    # bot_id = await bot_onj.id

    if message.left_chat_member.id == message.from_user.id:
        # если вышел сам
        await bot.send_message(
            686386017,
            f'{message.left_chat_member.get_mention(as_html=True)}'
            'вышел из чата.'
        )
        await bot.send_message(
            message.from_user.id,
            'Укажите причину выхода из проекта'
        )
    else:
        # если удален администратором
        pass
