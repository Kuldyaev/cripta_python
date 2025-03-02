from utils.useenv import get_from_env

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = "mysql+aiomysql://u0501959_super:VladA2004!@server177.hosting.reg.ru/u0501959_tapper"
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    BASE_URL = get_from_env("BASE_URL")
    TELEGRAM_BOT_TOKEN = get_from_env("TELEGRAM_BOT_TOKEN")
    ADMIN_ID = get_from_env("TELEGRAM_ADMIN_ID")
    
    def get_webhook_url(self) -> str:
        return f"{self.BASE_URL}/webhook"
    
config = Config() 