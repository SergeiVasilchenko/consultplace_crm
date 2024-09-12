import openai
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from data import config

storage = RedisStorage2(
    host=config.REDIS_HOST,
    port=int(config.REDIS_PORT),
    # password=config.REDIS_PASSWORD,
    db=int(config.REDIS_DB)

)
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

openai.api_key = config.AI_TOKEN
