from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/profile")
async def profile():
    return  {"Hello": "World"}

@app.post("/click")
async def click():
    return 0

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