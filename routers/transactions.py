from fastapi import APIRouter
import asyncio
from pydantic import BaseModel
from database.users import  user_exists,  update_user_transfer,  clear_user_hash
from database.assets import transfer_bank_exchange_spot, take_from_account

# lock = asyncio.Lock()

transactions_router = APIRouter(
   prefix="/transactions",
   tags=["Тransactions"],
)

class UserRequest(BaseModel):
    telegram_id: int
    transfer: float
    exchange_id: int
    hash: str | None
    

@transactions_router.post('/init')
async def init_demo_transaction(user_request: UserRequest)->str:
    # async with lock:  # Используем блокировку
        result2 = await transfer_bank_exchange_spot(telegram_id=user_request.telegram_id, 
                                                    exchange_id=user_request.exchange_id, 
                                                    volume=user_request.transfer, hash=user_request.hash)
        
        if(result2):
            # await update_user_transfer(user_id=user.id, transfer_value=0)
            # await clear_user_hash(user_id=user.id)
            return "ok"
        else:
            return "no"


class TransferRequest(BaseModel):
    telegram_id: int
    transfer: float
    exchange_id: int
    hash: str | None        
   
@transactions_router.post('/transfer')
async def init_demo_transaction(transfer_request: TransferRequest)->str: 
    result = user_exists(telegram_id=transfer_request.telegram_id)
    
    
    
    if(result):
        await update_user_transfer(user_id=user.id, transfer_value=0)
        await clear_user_hash(user_id=user.id)
        return "ok"
    else:
        return "no"       
    
    # if(user.transfer == user_request.transfer and user.transfer>0 and user.exchange == user_request.exchange_id):   
    #     result =await take_from_account(user_id=user.id, value=user_request.transfer)
    #     if(result):
    #         result2 = await transfer_bank_exchange_spot(user_id=user.id, 
    #                                             exchange_id=user_request.exchange_id, 
    #                                             volume=user_request.transfer)
    #         if(result2):
    #             await update_user_transfer(telegram_id=user_request.telegram_id, transfer_value=0)
    #             return "ok"
    #         else:
    #             return "no"
    #     else:
    #         return "no"
    # else:
    #     return "no"