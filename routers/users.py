from fastapi import APIRouter
from pydantic import BaseModel
from database.users import  get_user_by_telegram_id, get_userId_by_telegram_id
from database.coins import get_coins
from database.assets import get_account_balance

users_router = APIRouter(
   prefix="/users",
   tags=["Users"],
)
   
class UserRequest(BaseModel):
    telegram_id: int

@users_router.post('/me')
async def home_page(user_request: UserRequest):
    user_id = await get_userId_by_telegram_id(telegram_id=user_request.telegram_id)
    user_data = await get_user_by_telegram_id(user_request.telegram_id)
    balance = await get_account_balance(user_id=user_id)
    coins = await get_coins()
    coins_list = [ coin.name for coin in coins] 
    return {
            "data": user_data,
            "balance": balance,
            "coins": coins_list
            }