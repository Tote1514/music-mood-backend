from fastapi import APIRouter, Response, Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import requests
import secrets
from config import Settings

CLIENT_ID = Settings().SPOTIFY_CLIENT_ID
CLIENT_SECRET = Settings().SPOTIFY_CLIENT_SECRET
FRONTEND_URL = Settings().FRONTEND_URL
REDIRECT_URI = Settings().REDIRECT_URI
SCOPES = Settings().SPOTIFY_SCOPES.split()

session_store = {}

router = APIRouter(
    prefix="/auth",
)


@router.get("/login")
async def login(response: Response):

    state = secrets.token_urlsafe(16)
    session_store[state] = {"state": state}

    response.set_cookie(key="oauth_state", value=state, httponly=True, secure=False, samesite="lax")

    parameters = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": state,
        "show_dialog": "true"
    }

    auth_url = "https://accounts.spotify.com/authorize?" + \
                urlencode(parameters)

    return RedirectResponse(url=auth_url)

    
@router.get("/callback")
async def callback(code: str = None, state: str = None, error: str = None):
    stored_state = session_store.get(state)
    if not state or not stored_state or state != stored_state.get("state"):
        return RedirectResponse(url=f"{FRONTEND_URL}?error=state_mismatch")

    if error:
        return RedirectResponse(url=f"{FRONTEND_URL}?error={error}")

    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=missing_code")
    
    del session_store[state]

    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(token_url, data=payload, headers=headers)
    response_data = response.json()

    if response.status_code != 200:
        print(f"Spotify token exchange failed: {response.status_code} - {response_data}")
        return RedirectResponse(url=f"{FRONTEND_URL}?error=token_exchange_failed")

    access_token = response_data.get("access_token")
    refresh_token = response_data.get("refresh_token")

    user_info = await request_user_info(access_token)
    if not user_info:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=user_info_fetch_failed")
    
    display_name = user_info.get("display_name", "User")


    frontend_url = f"{FRONTEND_URL}/chat"
    redirect_url = f"{frontend_url}?display_name={display_name}"
    return RedirectResponse(url=redirect_url)

async def request_user_info(access_token: str):
    user_info_url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(user_info_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch user info: {response.status_code} - {response.text}")
        return None

    return response.json()
