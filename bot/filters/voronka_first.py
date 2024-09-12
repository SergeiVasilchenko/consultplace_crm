# from aiogram.dispatcher.filters import BoundFilter
# from aiogram import types
# from db_responce import log_get
#
# from data.config import URL_BASE
#
#
# class IsNewUser(BoundFilter):
#     async def check(self, message: types.Message):
#           res = log_get(
#               url=f'{URL_BASE}/detail-update/{message.from_user.username}/'
#            )
#           return res['education_status']
