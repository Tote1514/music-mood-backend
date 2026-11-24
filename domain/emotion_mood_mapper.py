"""Map individual emotions using the coordinates from the evaluation."""

from typing import Dict, List

from pathlib import Path

from domain.mood_mapper_strategy import MoodMapperStrategy
from schemas.mood_schema import Mood


class EmotionMoodMapper(MoodMapperStrategy):
    def __init__(self):
        """Initialize the emotion to coordinates mapping."""
        """Loading the values from pre-pcessed data"""
        emotion_data_path = Path(__file__).resolve().parents[1] / 'data/processed/emotions_values.csv'
        self.EMOTION_COORDINATES = {}
        with open(emotion_data_path, 'r') as f:
            next(f)  # Skip header
            for line in f:
                parts = line.strip().split(',')
                emotion = parts[0]
                energy = float(parts[1])
                valence = float(parts[2])
                self.EMOTION_COORDINATES[emotion] = {'energy': energy, 'valence': valence}

    def map(self, moods: List[Mood]) -> Dict[str, float]:
        """Average individual coordinates weighted by classifier scores.

        Receives original emotion labels, before grouping into broad moods.
        Combines all supported inputs; the classifier currently returns top-2.
        """
        valid_moods = [
            mood for mood in moods if mood.label in self.EMOTION_COORDINATES
        ]
        if not valid_moods:
            raise ValueError('No valid moods provided')

        total_score = sum(mood.score for mood in valid_moods)
        if total_score == 0:
            raise ValueError('Total mood score cannot be zero')

        return {
            axis: float(
                sum(
                    mood.score * self.EMOTION_COORDINATES[mood.label][axis]
                    for mood in valid_moods
                ) / total_score
            )
            for axis in ('energy', 'valence')
        }
