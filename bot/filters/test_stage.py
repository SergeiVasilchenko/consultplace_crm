from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import URL_BASE
from db_responce import log_get


class IsTestStage(BoundFilter):
    async def check(self, message: types.Message):
        res = log_get(url=f'{URL_BASE}/testtaskscores/')
        for item in res:
            if item['telegram_user_id'] == message.from_user.id:
                return item['score'] == 0
        return False
