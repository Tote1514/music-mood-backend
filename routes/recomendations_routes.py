from http import HTTPStatus

from fastapi import APIRouter, Depends

from data.track_dataset import TrackDataset
from dependencies.auth import get_access_token
from schemas.recommendation_schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/recommendations",
             status_code=HTTPStatus.OK,
             response_model=RecommendationResponse,
             summary="Recommend Spotify tracks based on the provided moods"
             )
async def recommend_tracks(request: RecommendationRequest,
                     access_token: str = Depends(get_access_token)):
    recommendation_service = RecommendationService(
        dataset=TrackDataset("data/processed/spotify-tracks-filtered.csv"),
        mood_mapper=...,
        access_token=access_token
    )
    return await recommendation_service.recommend(request.genres, request.moods)
