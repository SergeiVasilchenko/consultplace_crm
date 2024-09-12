async def on_startup(my_dp):
    import filters
    filters.setup(my_dp)

    import middlewares
    middlewares.setup(my_dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(my_dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(my_dp)

    print('Бот запущен')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
