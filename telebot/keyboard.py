
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from aiogram.utils.keyboard import  ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import Config

def app_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="WebApp", web_app=WebAppInfo(url="https://slavalion.github.io"))
    kb.adjust(1)
    return kb.as_markup()

def start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="начать тренировку", callback_data='start_learn' )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def start_keyboard_admin() -> InlineKeyboardMarkup:
    url_add_application = f"{Config.BASE_URL}/pages"
    kb = InlineKeyboardBuilder()
    kb.button(text="начать тренировку", callback_data='start_learn' )
    kb.button(text="admin dashboard",  web_app=WebAppInfo(url=url_add_application ))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def markets_keyboard(telegram_id:int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    print(telegram_id)
    kb.button(text="Спотовый рынок", web_app=WebAppInfo(url=f"https://slavalion.github.io?isSpot=true&me={telegram_id}") )
    kb.button(text="Деривативный рынок", web_app=WebAppInfo(url=f"https://slavalion.github.io?isSpot=false&me={telegram_id}"))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def exchanges_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="MEXC", callback_data='MEXC_m' )
    kb.button(text="ByBit", callback_data='ByBit_m' )
    kb.button(text="KuCoin", callback_data='KuCoin_m' )
    kb.button(text="BitGet", callback_data='BitGet_m' )
    kb.button(text="Huobi", callback_data='Huobi_m' )
    kb.button(text="BingX", callback_data='BingX_m' )
    kb.button(text="OKX", callback_data='OKX_m' )
    kb.button(text="BitMart", callback_data='BitMart_m' )
    kb.button(text="LBank", callback_data='LBank_m' )
    kb.button(text="CoinW", callback_data='CoinW_m' )
    kb.button(text="BitForex", callback_data='BitForex_m' )
    kb.button(text="BitFinex", callback_data='BitFinex_m' )
    kb.button(text="XT", callback_data='XT_m' )
    kb.button(text="DigitalFin", callback_data='DigitalFin_m' )
    kb.button(text="ProBit", callback_data='ProBit_m' )
    kb.button(text="Phemex", callback_data='Phemex_m' )
    kb.button(text="Tapbit", callback_data='Tapbit_m' )
    kb.button(text="AscendEX", callback_data='AscendEX_m' )
    kb.button(text="Poloniex", callback_data='Poloniex_m' )
    kb.button(text="Coinbase", callback_data='Coinbase_m' )
    kb.button(text="Kraken", callback_data='Kraken_m' )
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)