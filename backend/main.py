from fastapi import FastAPI, Query
import uvicorn
from models import *
from database import *


app = FastAPI()

@app.post("/")
async def start_login(username: str):
    if await asyncio.to_thread(user_exists, username):
        result = await asyncio.to_thread(get_user_sync, username)
    else:
        result = await asyncio.to_thread(create_user_sync, username)
    return result

@app.get("/profile")
async def profile(username: str = Query(..., description="Имя пользователя")):
    result = await asyncio.to_thread(get_user_sync, username)
    return result

@app.post("/click")
async def click(request: ClickRequest):
    username = request.username

    if await asyncio.to_thread(user_exists, username):
        await asyncio.to_thread(add_coins_sync, username, 1)
        await asyncio.to_thread(add_experience_sync, username, 1)
        user = await asyncio.to_thread(get_user_sync, username)
    else:
        user = await asyncio.to_thread(create_user_sync, username)

    return user

@app.get("/my_cards")
async def get_my_cards():
    return 0

@app.post("/card/buy")
async def buy_card_new():
    return 0

@app.get("/get/active/cards/shop")
async def shop_cards():
    return 0

@app.get("/my/dragon")
async def det_info_my_dragon():
    return 0

@app.post("/upgrades/my/dragon")
async def upgrades_dragon():
    return 0

@app.get("/get/active/battle")
async def get_battle():
    return 0

@app.post("/damage/attack")
async def damage():
    return 0

if __name__ == "__main__":
    uvicorn.run(app)