# import logging

from aiogram import types
# from data.config import admins_id
from filters import IsGroup
from loader import dp


@dp.message_handler(
    IsGroup(),
    content_types=types.ContentTypes.NEW_CHAT_MEMBERS
)
async def new_chat(message: types.Message):
    link = await dp.bot.create_chat_invite_link(chat_id=message.chat.id)
    for member in message.new_chat_members:
        await dp.bot.send_message(chat_id=message.chat.id,
                                  text=f"Салам, {member.first_name}, брат!")
        await dp.bot.send_message(
            chat_id=584748545,
            text=f"Пользователь @{member.username} добавлен в чат "
            f"-> {link.invite_link}"
        )


@dp.message_handler(
    IsGroup(),
    content_types=types.ContentTypes.LEFT_CHAT_MEMBER
)
async def left_chat(message: types.Message):
    link = await dp.bot.create_chat_invite_link(chat_id=message.chat.id)
    if message.from_user.id == message.left_chat_member.id:
        await dp.bot.send_message(
            chat_id=584748545,
            text=(
                f"Пользователь @{message.left_chat_member.username} съебал!\n"
                f"Из чата->{link}"
            )
        )
        await dp.bot.send_message(
            chat_id=message.left_chat_member.id,
            text=(
                f"не понял\n"
                f"причина побега из {link.invite_link}"
            )
        )
    else:
        await dp.bot.send_message(
            chat_id=584748545,
            text=(
                f"Пользователь @{message.left_chat_member.username}"
                f"был удален!\n Из чата->{link.invite_link}"
                f" пользователем @{message.from_user.username}"
            )
        )
        await dp.bot.send_message(
            chat_id=message.left_chat_member.id,
            text=(
                f"тебя кикнули из {message.chat.title} за неуплату!"
            )
        )
