from http import HTTPStatus

from fastapi import APIRouter

from schemas.recommendation_schemas import (
    RecommendationRequest,
    RecommendationResponse,
)

router = APIRouter()


@router.post("/recommendations",
             status_code=HTTPStatus.OK,
             response_model=RecommendationResponse,
             summary="Recommend Spotify tracks based on the provided moods"
             )
def recommend_tracks(request: RecommendationRequest):
    # Mocking response
    tracks = {
        "tracks": [
            {
                "name": "Palavras No Corpo",
                "artists": ["Palavras No Corpo"],
                "album_cover_url": "https://i.scdn.co/image/ab67616d0000485149c56bae9ff226e14a6463df",
                "spotify_url": "https://open.spotify.com/track/4xeP4rHORzLbJlaJVHWybQ",
                "uri": "spotify:track:27a1mYSG5tYg7dmEjWBcmL"
            },
            {
                "name": "Só Louco",
                "artists": ["Gal Costa"],
                "album_cover_url": "https://i.scdn.co/image/ab67616d00004851d940f0bee97f370629880123",
                "spotify_url": "https://open.spotify.com/track/2bLx1WMPGQKDme8WdGfpIs",
                "uri": "spotify:track:5Th1SPySWgYlkXXC6wLMwL"
            }
        ]
    }
    return RecommendationResponse(**tracks)
