from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import anaylisis_routes, auth_routes, playlist_routes, recomendations_routes,  user_routes

app = FastAPI()

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
app.include_router(user_routes.router)
app.include_router(playlist_routes.router)
app.include_router(anaylisis_routes.router)
app.include_router(recomendations_routes.router)


@app.get("/health")
async def read_health():
    return {"status": "ok"}
