from http import HTTPStatus

from fastapi import APIRouter

from schemas.mood_schema import MoodAnalysisRequest, MoodAnalysisResponse

router = APIRouter()


@router.post("/analysis",
             status_code=HTTPStatus.CREATED,
             response_model=MoodAnalysisResponse,
             summary="Analyze the mood of the provided text"
             )
def analyze_mood(request: MoodAnalysisRequest):
    # Placeholder for mood analysis logic
    # In a real implementation, this would call a service that analyzes the text and returns the moods
    moods = [
        {"label": "joy", "score": 0.87},
        {"label": "sadness", "score": 0.1},
        {"label": "anger", "score": 0.03}
    ]
    dominant_mood = max(moods, key=lambda x: x["score"])["label"]
    return MoodAnalysisResponse(moods=moods, dominant_mood=dominant_mood)
