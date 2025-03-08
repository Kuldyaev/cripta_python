from database import User, Exchange, new_session
from database.assets import create_deposit_new_user
from pydantic import BaseModel
from sqlalchemy.future import select  # Импортируем select для выполнения запроса
import hashlib

def create_hash(input_string):
    # Генерация хэша с использованием SHA-256
    hash_object = hashlib.sha256(input_string.encode())
    # Преобразование хэша в шестнадцатеричную строку
    hex_dig = hash_object.hexdigest()
    # Обрезка до 20 символов
    return hex_dig[:20]



class UserMeReturn(BaseModel):
    telegram_id: int
    name: str
    balance: float
    username: str
    exchange: int
    transfer: float




async def user_exists(telegram_id: int) -> bool:
   async with new_session() as session:
        # Создание запроса для проверки наличия пользователя с заданным id
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))  # Исправлено: используем session.execute
        user = result.scalars().first()  # Получаем первого пользователя, если он существует
        return user is not None  # Возвращаем True, если пользователь найден, иначе False
   
async def get_user_by_telegram_id(telegram_id: int) -> UserMeReturn:
   async with new_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))  # Исправлено: используем session.execute
        user = result.scalars().first()  
        return {
            'telegram_id': user.telegram_id,
            'name': user.name,
            # 'balance': user.balance,
            'username': user.username,
            'exchange': user.exchange,
            'transfer': user.transfer
        }

async def get_userId_by_telegram_id(telegram_id: int) -> int:
   async with new_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))  # Исправлено: используем session.execute
        return result.scalars().first().id
   
async def add_user(telegram_id, name, username) -> int:
   async with new_session() as session:
       new_user = User(telegram_id=telegram_id,name=name, username=username,
                       exchange=1, transfer=0)
       session.add(new_user)
       await session.flush()
       await session.commit()
       return new_user.id  


async def create_new_user(telegram_id, name, username)-> int:
    async with new_session() as session:
        new_user_id = await add_user(telegram_id=telegram_id, 
                       name=name, username=username
                       )
        await create_deposit_new_user(user_id=new_user_id)
        return new_user_id

async def get_user_hash(telegram_id: int) -> int | None:
   async with new_session() as session:
    # Создаем запрос для получения пользователя по telegram_id
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalars().first()  # Получаем первого пользователя из результата
    # Возвращаем баланс, если пользователь найден, иначе None
    return user.hash if user else None

async def get_user_exchange(telegram_id: int) -> int | None:
   async with new_session() as session:
    # Создаем запрос для получения пользователя по telegram_id
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalars().first()  # Получаем первого пользователя из результата
    # Возвращаем баланс, если пользователь найден, иначе None
    return user.exchange if user else None

async def update_user_exchange(telegram_id: int, exchange_value: int)-> None:
    async with new_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()  
        if user:
            user.exchange = exchange_value
            await session.commit()
        else:
            print("Пользователь с таким telegram_id не найден.")
            
async def update_user_transfer(user_id: int, transfer_value: float)-> None:
    async with new_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first() 
        if user:
            user.transfer = transfer_value
            user.hash = create_hash(str(user.name))
            await session.commit()
        else:
            print("Пользователь с таким telegram_id не найден.")
            
async def clear_user_hash(user_id: int):
   async with new_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first() 
        if user:
            user.hash = None
            await session.commit()
        else:
            print("Пользователь с таким id не найден.")
       
            
async def get_user_by_telegram_id(telegram_id: int) :
   async with new_session() as session:
    # Создаем запрос для получения пользователя по telegram_id
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalars().first()  
    return user if user else None