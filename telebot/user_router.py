from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from telebot.create_bot import bot
from telebot.keyboard import app_keyboard, start_keyboard, start_keyboard_admin, exchanges_keyboard
from database import  new_session
from database.users import user_exists, create_new_user, get_userId_by_telegram_id, update_user_exchange, get_user_exchange, update_user_transfer
from database.exchanges import get_name_exchange_by_id, get_id_exchange_by_code
from database.assets import get_account_balance
from config import config


user_router = Router()
    
    
@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    is_user_exist = await user_exists(telegram_id=message.from_user.id)
    
    if(is_user_exist):
        user_id = await get_userId_by_telegram_id(telegram_id = message.from_user.id)
        balance = await get_account_balance(user_id=user_id)
        # balance = await get_user_balance(message.from_user.id)
        await bot.send_message(message.from_user.id, f'Рады новой встрече, {message.from_user.first_name}!🥳.')
        if(message.from_user.id == config.ADMIN_ID or message.from_user.id == config.PROJECT_ADMIN_ID):
            await message.answer(
                    f"ДЕМО СЧЁТ\n  balance: {balance} USDT",
                    reply_markup=start_keyboard_admin()
               )
        else:
            await message.answer(
                    f"ДЕМО СЧЁТ\n  balance: {balance} USDT",
                    reply_markup=start_keyboard()
               )
        
    else:
        new_user_id = await create_new_user(telegram_id=message.from_user.id, 
                       name=message.from_user.first_name, 
                       username=message.from_user.username)
        print(f"Создан новый пользователь {new_user_id}")
        await bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}!🥳.')
        if(int(message.from_user.id) == int(config.ADMIN_ID) or int(message.from_user.id) == int(config.PROJECT_ADMIN_ID)):
            await message.answer(
                    f"ДЕМО СЧЁТ\n баланс: 1000 USDT",
                    reply_markup=start_keyboard_admin()
               )
        else:
            await message.answer(
                    f"ДЕМО СЧЁТ\n баланс: 1000 USDT",
                    reply_markup=start_keyboard()
               )

    
@user_router.message()
async def message_handler(message: Message):
    user_id = await get_userId_by_telegram_id(telegram_id = message.from_user.id)
    balance = await get_account_balance(user_id=user_id)
     # balance = await get_user_balance(message.from_user.id)
    exchange_id = await get_user_exchange(message.from_user.id)
    exchange = await get_name_exchange_by_id(exchange_id)
    try:
        number = float(message.text)
        if(number > balance):
            await bot.send_message(message.from_user.id, f'Недостаточно средств\n баланс: {balance} USDT \n ответным сообщением отправьте сумму перевода')
        elif (number > 0):
            await update_user_transfer(user_id=user_id, transfer_value=number)
            await message.answer(
                    f"ПЕРЕВОД\n {number} USD на биржу {exchange} \n Остаток на балансe: {balance - number} USD\n",
                    reply_markup=app_keyboard()
               )
        else:
            await bot.send_message(message.from_user.id, f'Число не может быть равно 0 или отрицательным\n баланс: {balance} USDT \n ответным сообщением отправьте сумму перевода')
    except ValueError:
        await message.delete() 
        await message.answer(
                    f"ДЕМО СЧЁТ\n баланс: {balance} USDT",
                    reply_markup=start_keyboard()
               )


@user_router.callback_query(lambda c: c.data in ['start_learn', 'spot_matket', 'futures_matket'])
async def callback_query_handler(callback_query: types.CallbackQuery)-> None:
    if callback_query.data == 'start_learn':
        # await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
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
    # balance = await get_user_balance(callback_query.from_user.id)
    user_id = await get_userId_by_telegram_id(telegram_id = callback_query.from_user.id)
    balance = await get_account_balance(user_id=user_id)
    exchange_id = await get_id_exchange_by_code(callback_query.data)
    exchange = callback_query.data[:-2]
    await update_user_exchange(telegram_id=callback_query.from_user.id, exchange_value=exchange_id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id) 
    await bot.send_message(callback_query.from_user.id, f'Выбрана биржа {exchange}\n баланс: {balance} USDT \n ответным сообщением отправьте сумму перевода для сделок')
    
    # reply_markup=app_keyboard())
