
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from aiogram.utils.keyboard import  ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import Config

def app_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # if is_new_user:
    #      url_add_application = f"{Config.BASE_URL}pages?user_id={user_id}"
    #      kb.button(text="Участвовать", callback_data="participate")
    # else:
    url_add_application = f"{Config.BASE_URL}/pages"
    kb.button(text="WebApp", web_app=WebAppInfo(url="https://slavalion.github.io"))

    kb.adjust(1)
    return kb.as_markup()

def start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="начать тренировку", callback_data='start_learn' )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def markets_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Спотовый рынок", callback_data='spot_matket' )
    kb.button(text="Деривативный рынок", callback_data='futures_matket' )
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def exchanges_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="MEXC", callback_data='MEXC_m' )
    kb.button(text="ByBit", callback_data='ByBit_m' )
    kb.button(text="KuCoin", callback_data='KuCoin_m' )
    kb.button(text="BitGet", callback_data='BitGet_m' )
    kb.button(text="Kraken", callback_data='Kraken_m' )
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)