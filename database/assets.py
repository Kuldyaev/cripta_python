from database import Asset, new_session
from pydantic import BaseModel
from sqlalchemy import select, and_

class AssetsItem(BaseModel):
    id: int
    name: str
    code: str

async def create_deposit_new_user(user_id: int) -> int:
    async with new_session() as session:
        new_asset = Asset(user_id=user_id,market_id=1, exchange_id=None,
                       coin_id=1, volume=1000)
        session.add(new_asset)
        await session.flush()
        await session.commit()
        return new_asset.id  
    
async def get_account_balance(user_id: int)->float: 
    async with new_session() as session:
        account = await session.execute(select(Asset).where(and_(Asset.user_id == user_id, 
                                                                 Asset.exchange_id == None)))
        return account.scalars().first().volume
    
async def take_from_account(user_id: int, value: float)->bool: 
    async with new_session() as session:
        account = await session.execute(select(Asset).where(and_(Asset.user_id == user_id, 
                                                                 Asset.exchange_id == None)))
        balance = account.scalars().first()
        prev_balance = balance.volume
        if(prev_balance > value):
            balance.volume = prev_balance - value
            await session.commit()
            return True
        else:
            return False
    
async def transfer_bank_exchange_spot(user_id: int, exchange_id: int, volume: float ) -> bool:
   async with new_session() as session:
        asset_exist = await session.execute(select(Asset).where(and_(Asset.user_id == user_id, 
                                                                     Asset.exchange_id == exchange_id, 
                                                                     Asset.market_id==2)))
        asset = asset_exist.scalars().first()
        if(asset):
            debit_account = await take_from_account(user_id=user_id, value=volume)
            if(debit_account):
                prev_volume = asset.volume
                asset.volume = prev_volume + volume
                await session.commit()
                return True
            else:
                return False
        else:
            debit_account = await take_from_account(user_id=user_id, value=volume)
            if(debit_account):
                new_asset = Asset(user_id=user_id,market_id=2, exchange_id=exchange_id,
                       coin_id=2, volume=volume)    
                session.add(new_asset)
                await session.flush()
                await session.commit()
                return True
            else:
                return False