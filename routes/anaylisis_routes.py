from http import HTTPStatus

from fastapi import APIRouter

from schemas.mood_schema import MoodAnalysisRequest, MoodAnalysisResponse
from services.mood_services import MoodGenerator

router = APIRouter()

mood_generator = MoodGenerator()


@router.post(
    "/analysis",
    status_code=HTTPStatus.CREATED,
    response_model=MoodAnalysisResponse,
    summary="Analyze the mood of the provided text"
)
def analyze_mood(request: MoodAnalysisRequest):
    result = mood_generator.process_texts([request.text])

    return result[0]
