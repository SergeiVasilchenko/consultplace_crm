from aiogram import Dispatcher

from .group import IsGroup
from .new_user import IsNewUser
from .prived import IsPrivate
from .test_stage import IsTestStage


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsNewUser)
    dp.filters_factory.bind(IsTestStage)
