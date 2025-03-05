from database import Exchange, new_session
from pydantic import BaseModel
from sqlalchemy.future import select

class ExchangeItem(BaseModel):
    id: int
    name: str
    code: str

async def get_id_exchange_by_code(code: str) -> int:
   async with new_session() as session:
        result  = await session.execute(select(Exchange).where(Exchange.code == code)) 
        my_id = result.scalars().first()
        return my_id.id
    
async def get_name_exchange_by_id(id: int) -> str:
   async with new_session() as session:
        result  =  await session.execute(select(Exchange).where(Exchange.id == id)) 
        ex = result.scalars().first()  
        return  ex.name    

async def get_image_exchange_by_id(id: int) -> str:
   async with new_session() as session:
        result  =  await session.execute(select(Exchange).where(Exchange.id == id)) 
        ex = result.scalars().first()  
        return  ex.img    
