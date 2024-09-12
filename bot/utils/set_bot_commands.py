from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand(command='start', description='Запустить бота'),
        types.BotCommand(command='help', description='Помощь'),
        types.BotCommand(command='id', description='Узнать свой ID'),
        types.BotCommand(command='pay', description='Оплати подписку 💳')
    ])
