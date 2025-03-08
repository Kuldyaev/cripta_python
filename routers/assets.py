from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from database.users import  get_user_by_telegram_id
from database.exchanges import  get_image_exchange_by_id
from database.assets import get_assets_by_userId

assets_router = APIRouter(
   prefix="/assets",
   tags=["Assets"],
)
   
class AssetsRequest(BaseModel):
    telegram_id: int
    exchange_id: int

class AssetsResponce(BaseModel):
    id: int
    market_id: int
    volume: float

@assets_router.post('/')
async def home_page(user_request: AssetsRequest)->List[AssetsResponce]:
    user = await get_user_by_telegram_id(user_request.telegram_id)
    exchange_data = await get_assets_by_userId (user_id=user.id, exchange_id=user_request.exchange_id)
    result = [{"id":item.coin_id, "market_id":item.market_id, 'volume': item.volume} for item in exchange_data]
    print(result)
    return result