from http import HTTPStatus
import httpx
from fastapi import APIRouter, HTTPException, Depends

from schemas.user_schema import UserResponse
from dependencies.auth import get_access_token

router = APIRouter(prefix="/user")


@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get the user's Spotify profile information",
    status_code=HTTPStatus.OK,
)
async def get_user_info(access_token: str = Depends(get_access_token)):

    user_info_url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, headers=headers)

    if response.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch user info from Spotify"
        )

    display_name = response.json().get("display_name", "User")

    return {"display_name": display_name}