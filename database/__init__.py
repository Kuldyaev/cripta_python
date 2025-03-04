from config import Config
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Создание асинхронного движка
engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# new_session = async_sessionmaker(engine, expire_on_commit=False)

# Создание сессии
new_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Model(DeclarativeBase):
   pass

class User(Model):
   __tablename__ = "users"
   id: Mapped[int] = mapped_column(primary_key=True)
   telegram_id: Mapped[int | None]
   name: Mapped[str | None] = mapped_column(String(255))
   familyname: Mapped[str | None] = mapped_column(String(255))
   balance: Mapped[int]

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