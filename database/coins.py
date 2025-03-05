from database import Coin, new_session
from sqlalchemy.future import select
from typing import List

async def get_coins() -> List[Coin]:
   async with new_session() as session:
        result  = await session.execute(select(Coin))
        coins = result.scalars().all()  # Получаем все объекты Coin
        return coins

