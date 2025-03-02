from fastapi import Request
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from config import Config, config

# bot_router = Router()

# @bot_router.message(CommandStart())
# async def cmd_start(message: Message) -> None:
#     await bot.send_message(Config.ADMIN_ID, f'Test Start🥳.')

   
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))    

dp = Dispatcher(storage=MemoryStorage())  


async def start_bot():
    try:
        await bot.send_message(config.ADMIN_ID, f'Я запущен🥳.')
    except:
        pass


async def stop_bot():
    try:
        await bot.send_message(config.ADMIN_ID, 'Бот остановлен. За что?😔')
    except:
        pass
    
async def feed_update_bot(request: Request) -> None:
    try:
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
    except:
        pass