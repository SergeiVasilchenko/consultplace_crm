from aiogram import types
from aiogram.types import ContentTypes
from filters import IsPrivate
from keyboards.inline import subscription
from loader import dp
from utils.misc import rate_limit


# оплата
@dp.message_handler(IsPrivate(), commands=['pay17'])
async def command_pay(message: types.Message):
    text = ('В подписку входит:\n'
            '2 лекции от экспертов: VC и консалтинг\n'
            'Минимум 1 практический проект в месяц\n'
            'Инструкция и вспомогательные материалы для выполнения\n'
            '2 встречи с проектным менеджером\n'
            'NFT-сертификат через 4 месяца подписки\n'
            'Портфолио через 6 месяцев подписки\n'
            'CV через 9 месяцев подписки\n\n'
            'Варианты подписки:\n'
            '1 месяц — 5.000₽/мес.\n'
            '3 месяца — 13.500₽ (4.500₽/мес.)\n'
            '6 месяцев — 24.000₽ (4.000₽/мес.)\n'
            '12 месяцев — 42.000₽ (3.500₽/мес.)')
    await message.answer(text=text, reply_markup=subscription)

    # await message.answer(text="Выбери тариф:")
    # prices = [types.LabeledPrice(label="1 месяц", amount=50000),
    #           types.LabeledPrice(label="3 месяца (4.500₽/мес.)", amount=135000),
    #           types.LabeledPrice(label="6 месяцев (4.000₽/мес.)", amount=240000),
    #           types.LabeledPrice(label="12 месяцев (3.500₽/мес.)", amount=42000)]
    # await dp.bot.send_invoice(chat_id=message.chat.id,
    #                           title="hellow1",
    #                           description="hellow2",
    #                           provider_token="381764678:TEST:84282",
    #                           currency="RUB",
    #                           prices=prices,
    #                           payload="hellow3",
    #                           photo_url="https://consultplace.sytes.net/media/Files/logo_login.jpg"
    #                           )


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                           error_message="Aliens tried to steal your card's CVV,"
                                                         " but we successfully protected your credentials,"
                                                         " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(IsPrivate(), content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await dp.bot.send_message(message.chat.id,
                              'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                              ' as fast as possible! Stay in touch.'
                              '\n\nUse /buy again to get a Time Machine for your friend!'.format(
                                  message.successful_payment.total_amount / 100, message.successful_payment.currency),
                              parse_mode='Markdown')
