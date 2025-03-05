from fastapi import APIRouter, Request
from database.assets import transfer_bank_exchange_spot, take_from_account


transactions_router = APIRouter(
   prefix="/transactions",
   tags=["Тransactions"],
)



@transactions_router.post('/init')
async def init_demo_transaction(request: Request)->str:
    # result = await take_from_account(user_id=2, value=50)
    
    result = await transfer_bank_exchange_spot(user_id=2, exchange_id=1, volume=50)
    return str(result)