import requests
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import URL_BASE


class IsNewUser(BoundFilter):
    async def check(self, message: types.Message):
        res = requests.get(
            url=f'{URL_BASE}/detail-update/{message.from_user.username}/'
        )
        return res.status_code == 404
