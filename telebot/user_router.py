from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from telebot.create_bot import bot
from telebot.keyboard import app_keyboard
from config import config


user_router = Router()
    
    
@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await bot.send_message(config.ADMIN_ID, f'Start🥳.',
                    reply_markup=app_keyboard())
    
@user_router.message()
async def message_handler(message: Message):
   await message.answer(
                    f"Добро пожаловать , присоединяйтесь к нашему проекту!\n",
                    reply_markup=app_keyboard()
               )

# reply_markup=app_keyboard(user_id=message.from_user.id, is_new_user=False))
