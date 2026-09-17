from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from data.track_dataset import TrackDataset
from dependencies.auth import get_access_token
from domain.emotion_mood_mapper import EmotionMoodMapper
from schemas.recommendation_schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from services.recommendation_service import RecommendationService

router = APIRouter()
DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / 'data/processed/spotify-music-features-filtered.csv'
)


@router.post(
    '/recommendations',
    status_code=HTTPStatus.OK,
    response_model=RecommendationResponse,
    summary='Recommend Spotify tracks based on the provided moods',
)
async def recommend_tracks(
    request: RecommendationRequest,
    access_token: str = Depends(get_access_token),
):
    recommendation_service = RecommendationService(
        dataset=TrackDataset(DATASET_PATH),
        mood_mapper=EmotionMoodMapper(),
        access_token=access_token,
    )
    try:
        # No genre filtering; preserve compatibility with existing requests.
        return await recommendation_service.recommend([], request.moods)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
