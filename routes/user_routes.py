from http import HTTPStatus

from fastapi import APIRouter, Depends

from dependencies.auth import get_access_token
from schemas.user_schema import UserResponse
from services.spotify_services import spotify

router = APIRouter(prefix="/user")


@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get the user's Spotify profile information",
    status_code=HTTPStatus.OK,
)
async def get_user_info(access_token: str = Depends(get_access_token)):
        return await spotify.get_user_profile(access_token)
