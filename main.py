from fastapi import FastAPI

from database.database import engine, Base
from models import User  

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}