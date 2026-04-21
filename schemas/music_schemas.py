from typing import List, Optional

from pydantic import BaseModel, Field


class PlaylistCreateRequest(BaseModel):
    name: str = Field(..., example="Sad vibes")
    description: Optional[str] = Field(
                            None,
                            example="Playlist para momentos introspectivos")
    track_uris: List[str] = Field(...,
                                example=["spotify:track:123",
                                         "spotify:track:456"])


class TrackResponse(BaseModel):
    name: str
    artists: List[str]
    album_cover_url: str
    spotify_url: str
    uri: str


class TrackListResponse(BaseModel):
    tracks: List[TrackResponse]


class PlaylistResponse(BaseModel):
    id: str
    url: str
    name: str
