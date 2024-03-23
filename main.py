from fastapi import FastAPI
from presentation import routers


app = FastAPI()
app.include_router(routers.product_router)


@app.get("/")
async def root():
    return {"message": "meowdy!"}
