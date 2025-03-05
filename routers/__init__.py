from fastapi import APIRouter
from .pages import pages_router
from .users import users_router
from .exchange import exchange_router
from .transactions import transactions_router
from .coins import coins_router


router = APIRouter()
router.include_router(pages_router)
router.include_router(users_router)
router.include_router(exchange_router)
router.include_router(transactions_router)
router.include_router(coins_router)