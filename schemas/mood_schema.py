from typing import List

from pydantic import BaseModel, Field


class Mood(BaseModel):
    label: str = Field(..., example="joy")
    score: float = Field(..., ge=0, le=1, example=0.87)


class MoodAnalysisRequest(BaseModel):
    text: str = Field(..., example="Hoje foi um dia incrível!")


class MoodAnalysisResponse(BaseModel):
    moods: List[Mood]
    dominant_mood: str
