from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import engine, Base
from models import User 
from config import Settings
from routes import auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

settings = Settings()

origins = [
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}