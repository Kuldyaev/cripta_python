from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from aiogram.types import Message, Update
from contextlib import asynccontextmanager
from routers import router as api_router
from telebot.create_bot import bot, dp, stop_bot, start_bot 
from telebot.user_router import user_router
from database import create_tables, delete_tables, insert_objects
from config import config
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await insert_objects()
    # Код, выполняющийся при запуске приложения
    dp.include_router(user_router)
    await start_bot()
    webhook_url = config.get_webhook_url()  
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    print(f"Webhook set to {webhook_url}")
    yield  # Приложение работает
    # Код, выполняющийся при завершении работы приложения
    await delete_tables()
    await bot.delete_webhook()
    await stop_bot()
    print("Webhook removed")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
   CORSMiddleware, 
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"], 
)

templates = Jinja2Templates(directory='templates')

app.include_router(api_router)
    
@app.get("/")
async def home_page(request: Request):
   return templates.TemplateResponse(name='home.html', context={'request': request})


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")

@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)



if __name__ == "__main__":    
   uvicorn.run(app, host='0.0.0.0', log_level='info')