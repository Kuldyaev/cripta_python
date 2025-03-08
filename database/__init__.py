from config import config
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.future import select
from sqlalchemy.sql import func
from datetime import datetime 


# Создание асинхронного движка
engine = create_async_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

# new_session = async_sessionmaker(engine, expire_on_commit=False)

# Создание сессии
new_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Model(DeclarativeBase):
   pass

class Market(Model):
   __tablename__ = "markets"
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str | None] = mapped_column(String(10)) 
   
class Coin(Model):
   __tablename__ = "coins"
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str | None] = mapped_column(String(10)) 

class Exchange(Model):
   __tablename__ = "exchanges"
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str | None] = mapped_column(String(255))
   code: Mapped[str | None] = mapped_column(String(255))
   img: Mapped[str | None] = mapped_column(String(8000))

class User(Model):
   __tablename__ = "users"
   id: Mapped[int] = mapped_column(primary_key=True)
   telegram_id: Mapped[int | None]
   name: Mapped[str | None] = mapped_column(String(255))
   username: Mapped[str | None] = mapped_column(String(255))
   hash: Mapped[str | None] = mapped_column(String(20), default=None)
   exchange: Mapped[int] = mapped_column(ForeignKey("exchanges.id"))
   transfer: Mapped[float]

class Asset(Model):
   __tablename__ = "assets"
   id: Mapped[int] = mapped_column(primary_key=True)
   user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
   market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"))
   exchange_id: Mapped[int | None] = mapped_column(ForeignKey("exchanges.id"))
   coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
   volume: Mapped[float]
   
class Transaction(Model): 
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    asset_out: Mapped[int | None] = mapped_column(ForeignKey("assets.id"))
    asset_in: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    volume: Mapped[float]
    hash: Mapped[str | None] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

#
# class UserDetails(Model):
#    __tablename__ = "user_details"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#    name: Mapped[str | None] = mapped_column(String(255))
#    familyname: Mapped[str | None] = mapped_column(String(255))

   
# class GamerDetails(Model):
#    __tablename__ = "gamer_details"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#    coins: Mapped[int]
#    energy: Mapped[int]
#    level: Mapped[int]
   
async def create_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)
       
async def insert_objects() -> None:
    logo_ByBit = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4QLgRXhpZgAATU0AKgAAAAgAAwExAAIAAAAhAAABPodpAAQAAAABAAABYOocAAcAAAEMAAAAMgAAAAAc6gAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQWRvYmUgSWxsdXN0cmF0b3IgMjYuMyAoV2luZG93cykAAAAFkAMAAgAAABQAAAKukAQAAgAAABQAAALCkpEAAgAAAAMwMAAAkpIAAgAAAAMwMAAA6hwABwAAAQwAAAGiAAAAABzqAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAyMDIzOjAzOjIxIDEzOjU5OjM2ADIwMjM6MDM6MjEgMTM6NTk6MzYAAAD/4QLfaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCc/Pg0KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyI+PHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj48cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0idXVpZDpmYWY1YmRkNS1iYTNkLTExZGEtYWQzMS1kMzNkNzUxODJmMWIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+PHhtcDpDcmVhdG9yVG9vbD5BZG9iZSBJbGx1c3RyYXRvciAyNi4zIChXaW5kb3dzKTwveG1wOkNyZWF0b3JUb29sPjx4bXA6Q3JlYXRlRGF0ZT4yMDIzLTAzLTIxVDEzOjU5OjM2PC94bXA6Q3JlYXRlRGF0ZT48L3JkZjpEZXNjcmlwdGlvbj48L3JkZjpSREY+PC94OnhtcG1ldGE+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPD94cGFja2V0IGVuZD0ndyc/Pv/bAEMAAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAgIBAQIBAQECAgICAgICAgIBAgICAgICAgICAv/bAEMBAQEBAQEBAQEBAQIBAQECAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAv/AABEIAFAAUAMBIgACEQEDEQH/xAAfAAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv/xAC1EAACAQMDAgQDBQUEBAAAAX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUmJygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaH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"
    logo_kraken = "data:image/jpeg;base64,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"
    logo_MEXC = 'data:image/jpeg;base64,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'
    img = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAeAB4AAD/2wBDAAkGBwgHBgkICAgKCgkLDhcPDg0NDhwUFREXIh4jIyEeICAlKjUtJScyKCAgLj8vMjc5PDw8JC1CRkE6RjU7PDn/2wBDAQoKCg4MDhsPDxs5JiAmOTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTn/wAARCABQAFADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDw2iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDqfBXgfUPGMGpvp80Ky2EYfynzmUndhVx3+Xv61Ut/DF1P4VutfEqBLe8Wza3KnzC5AP9a6n4ZXtxp3hDxpe2kpiuIIbaSNweQwkJFddq+oaU/w9HiayVVivtYtr26tl/5ZTLgSKPqVz+NAHHJ8LhDLbWGpeJ9LsNauVDR2Em4sCfuqzDgE+n5ZriNZ0u70XVLnTb+Lyrq2cpIuc8+oPcHrXqni3wJrXiXx7/bukGK50e/eOdL5Zl2RIFXOec8Yrjvi3qtprPj7U7uxkWS3BSISLyHKqFJHqMg0AZni/wAMz+Fr21tbi4ina5tUuQYwQAGzgHPfitHw34HbVNEfXNT1a00fSvM8qOe4BYyv3CqOT/8Ar9DXdfEvwL4j8S6jpN7pGn/abddMgjL+ci/MMkjBI9RWdNol94s+GmkaZo6JNqehXM0V5ZCRQ/zMcMMnBH+J9KAOU8QeA9S0u90yKzmh1S21UgWVzanKynIGOehGf881sH4XF7p9Kt/E2kza9GpLaepYHcBkqH6Fvaut0+8tfA1t4H0XXJ4VvoL2W5uUDhvsqOrqu4jpy4P4GmaH4Alh8Y6g3iDRLe90u8uTJDqjX5iVFZiRtCnLMxZRj1oA888M+CLnWLa+v769t9I0yxfyp7m6zgSf3Ao5J/xpvivwXLoWnWurWmo22q6RdMY0u7fICuP4WU9DwfyrtV0o+IvBGteF9D2HUNM1uWdbQyANLDkqCCTzj+nuKoa7YTeEfhP/AGHq7JHquo6gLlLTeGaKMKBuOOmcfr9aAPMgzKCAxAPUA9aN7bdm47Sc4zxTaKAJUuZ0iaFZpFibqgYhT+FRUUUASi4nHSaT/vo0kU0sMnmRSvG/95WIP51HRQA53aRi7sWY8kk5Jp5uJ2jWMzSGNDlVLHC/QVFRQA+OWSOQSJIyuOQynB/OiWWSZy8rs7nqzHJNMooAKKKKACiiigAooooAKKKKACiiigD/2Q=="
    
    
    async with new_session() as session:
        async with session.begin():
            session.add_all(
                [
                    Exchange(name="MEXC", code='MEXC_m', img=logo_MEXC),
                    Exchange(name="ByBit", code='ByBit_m', img=logo_ByBit),
                    Exchange(name="KuCoin", code='KuCoin_m', img=img),
                    Exchange(name="BitGet", code='BitGet_m', img=img),
                    Exchange(name="Huobi", code='Huobi_m', img=img),
                    Exchange(name="BingX", code='BingX_m', img=img),
                    Exchange(name="OKX", code='OKX_m', img=img),
                    Exchange(name="BitMart", code='BitMart_m' , img=img),
                    Exchange(name="LBank", code='LBank_m', img=img),
                    Exchange(name="CoinW", code='CoinW_m', img=img),
                    Exchange(name="BitForex", code='BitForex_m', img=img),
                    Exchange(name="BitFinex", code='BitFinex_m', img=img),
                    Exchange(name="XT", code='XT_m', img=img),
                    Exchange(name="DigitalFin", code='DigitalFin_m', img=img),
                    Exchange(name="ProBit", code='ProBit_m', img=img),
                    Exchange(name="Phemex", code='Phemex_m', img=img),
                    Exchange(name="Tapbit", code='Tapbit_m', img=img),
                    Exchange(name="AscendEX", code='AscendEX_m', img=img),
                    Exchange(name="Poloniex", code='Poloniex_m', img=img),
                    Exchange(name="Coinbase", code='Coinbase_m', img=img),
                    Exchange(name="Kraken", code='Kraken_m', img=logo_kraken),
                    Market(name="account"),
                    Market(name="spot"),
                    Market(name="futures"),
                    Coin(name="USD"),
                    Coin(name="USDT"),
                    Coin(name="BTC"),
                    Coin(name="ETH"),
                    Coin(name="SOL"),
                    Coin(name="BNB"),
                    Coin(name="DOGE"),
                    Coin(name="ADA"),
                    User(telegram_id=7894658,name="Mefistofel", username="Diablo",
                       exchange=1, transfer=300)
                ]
            )
