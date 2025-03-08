from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from database.coins import get_coins


coins_router = APIRouter(
   prefix="/coins",
   tags=["Coins"],
)

class CoinType(BaseModel):
    name: str
    id: int

@coins_router.get('/')
async def get_coins_arr()->List[CoinType]:
   coins = await get_coins()
   results = [{"name": coin.name, "id": coin.id} for coin in coins]
   return results

@coins_router.get('/list')
async def get_coins_list()->List[str]:
   coins = await get_coins()
   results = [ coin.name for coin in coins] 
   return results