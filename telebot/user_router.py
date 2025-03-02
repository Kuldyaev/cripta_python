from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from telebot.create_bot import bot
from telebot.keyboard import app_keyboard, start_keyboard, markets_keyboard, exchanges_keyboard
from config import config


user_router = Router()
    
    
@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await bot.send_message(config.ADMIN_ID, f'Start🥳.',
                    reply_markup=app_keyboard())
    
@user_router.message()
async def message_handler(message: Message):
    await message.answer(
                    f"ДЕМО СЧЁТ\n баланс: 1000 USDT",
                    reply_markup=start_keyboard()
               )


@user_router.callback_query(lambda c: c.data in ['start_learn', 'spot_matket', 'futures_matket'])
async def callback_query_handler(callback_query: types.CallbackQuery)-> None:
    if callback_query.data == 'start_learn':
        await bot.send_message(callback_query.from_user.id, f'Выбор рынка💰.',
                    reply_markup=markets_keyboard())
    if callback_query.data == 'spot_matket':
        await bot.send_message(callback_query.from_user.id, f'Выбор биржи💹.',
                    reply_markup=exchanges_keyboard())
    if callback_query.data == 'futures_matket':
        await bot.send_message(callback_query.from_user.id, f'Выбор биржи💹.',
                    reply_markup=exchanges_keyboard())
        
@user_router.callback_query(lambda c: c.data in ['MEXC_m', 'ByBit_m', 'KuCoin_m', 'BitGet_m', 'Kraken_m' ])
async def callback_exchange_handler(callback_query: types.CallbackQuery)-> None:
    await bot.send_message(callback_query.from_user.id, f'Приступим 🥳.',
                    reply_markup=app_keyboard())
