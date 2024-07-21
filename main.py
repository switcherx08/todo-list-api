from fastapi import FastAPI

from api import api_router
from database import db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await db.init_tables()

app.include_router(api_router, prefix='/api')
