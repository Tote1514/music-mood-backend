
from typing import List

from pydantic import BaseModel

from .mood_schema import Mood
from .music_schemas import Track


class RecommendationRequest(BaseModel):
    moods: List[Mood]
    genres: List[str] = []


class RecommendationResponse(BaseModel):
    tracks: List[Track]
