from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from telebot.create_bot import bot
from telebot.keyboard import app_keyboard, start_keyboard, markets_keyboard, exchanges_keyboard
from config import config


user_router = Router()
    
    
@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await bot.send_message(message.from_user.id, f'Добро пожаловать!🥳.')
    await message.answer(
                    f"ДЕМО СЧЁТ\n баланс: 1000 USDT",
                    reply_markup=start_keyboard()
               )
    
@user_router.message()
async def message_handler(message: Message):
    await message.delete() 
    await message.answer(
                    f"ДЕМО СЧЁТ\n баланс: 1000 USDT",
                    reply_markup=start_keyboard()
               )


@user_router.callback_query(lambda c: c.data in ['start_learn', 'spot_matket', 'futures_matket'])
async def callback_query_handler(callback_query: types.CallbackQuery)-> None:
    if callback_query.data == 'start_learn':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f'Выбор биржи💹.',
                    # reply_markup=markets_keyboard())
                    reply_markup=exchanges_keyboard())
    if callback_query.data == 'spot_matket':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f'Выбор биржи💹.',
                    reply_markup=exchanges_keyboard())
    if callback_query.data == 'futures_matket':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f'Выбор биржи💹.',
                    reply_markup=exchanges_keyboard())
        
@user_router.callback_query(lambda c: c.data in ['MEXC_m', 'ByBit_m', 'KuCoin_m', 'BitGet_m',
                                                 "Huobi_m", "BingX_m", "OKX_m", "BitMart_m",
                                                 'LBank_m', 'CoinW_m',  'BitForex_m', 'BitFinex_m',
                                                 'XT_m', 'DigitalFin_m', 'ProBit_m', 'Phemex_m',
                                                 'Tapbit_m', 'AscendEX_m', 'Poloniex_m', 'Coinbase_m',
                                                 'Kraken_m' ])
async def callback_exchange_handler(callback_query: types.CallbackQuery)-> None:
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id) 
    await bot.send_message(callback_query.from_user.id, f'Приступим 🥳.',
                    reply_markup=app_keyboard())
