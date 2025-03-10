from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

pages_router = APIRouter(
   prefix="/pages",
   tags=["Pages"],
)

templates = Jinja2Templates(directory='templates')

@pages_router.get('/')
async def home_page(request: Request):
   return templates.TemplateResponse(name='first.html', context={'request': request})
