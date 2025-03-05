from fastapi import APIRouter
from pydantic import BaseModel
from database.exchanges import  get_image_exchange_by_id

exchange_router = APIRouter(
   prefix="/exchange",
   tags=["Exchange"],
)
   
class UserRequest(BaseModel):
    exchange_id: int

@exchange_router.post('/img')
async def home_page(user_request: UserRequest):
    exchange_data = await get_image_exchange_by_id(user_request.exchange_id)
    return exchange_data