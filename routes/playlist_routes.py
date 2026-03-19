from http import HTTPStatus

from fastapi import APIRouter, Depends

from dependencies.auth import get_access_token
from schemas.music_schemas import PlaylistCreateRequest, PlaylistResponse
from services.spotify_services import spotify

router = APIRouter()


@router.post("/playlist",
             status_code=HTTPStatus.CREATED,
             response_model=PlaylistResponse,
             summary="Create a new Spotify playlist"
             )
async def create_playlist(music_requests: PlaylistCreateRequest,
                          access_token: str = Depends(get_access_token)
                          ):
    playlist = spotify.create_playlist(access_token,
                                       music_requests.name,
                                       music_requests.description,
                                       music_requests.track_uris)
    return PlaylistResponse(**playlist)
