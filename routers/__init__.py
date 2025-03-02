from fastapi import APIRouter
from .pages import pages_router



router = APIRouter()
router.include_router(pages_router)
