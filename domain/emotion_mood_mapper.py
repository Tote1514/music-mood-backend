"""Map individual emotions using the coordinates from the evaluation."""

from typing import Dict, List

from domain.mood_mapper_strategy import MoodMapperStrategy
from schemas.mood_schema import Mood


class EmotionMoodMapper(MoodMapperStrategy):
    # Theoretical coordinates, not values learned by the classifier.
    EMOTION_COORDINATES = {
        'admiração': {'valence': 0.70, 'energy': 0.30},
        'diversão': {'valence': 0.80, 'energy': 0.80},
        'raiva': {'valence': -0.80, 'energy': 0.90},
        'aborrecimento': {'valence': -0.50, 'energy': 0.30},
        'aprovação': {'valence': 0.50, 'energy': 0.10},
        'zelo': {'valence': 0.60, 'energy': -0.10},
        'confusão': {'valence': -0.35, 'energy': 0.25},
        'curiosidade': {'valence': 0.35, 'energy': 0.45},
        'desejo': {'valence': 0.55, 'energy': 0.55},
        'decepção': {'valence': -0.65, 'energy': -0.35},
        'desaprovação': {'valence': -0.55, 'energy': 0.15},
        'nojo': {'valence': -0.75, 'energy': 0.40},
        'constrangimento': {'valence': -0.55, 'energy': 0.35},
        'entusiasmo': {'valence': 0.80, 'energy': 0.90},
        'medo': {'valence': -0.85, 'energy': 0.85},
        'gratidão': {'valence': 0.75, 'energy': -0.10},
        'luto': {'valence': -0.90, 'energy': -0.75},
        'alegria': {'valence': 0.85, 'energy': 0.60},
        'amor': {'valence': 0.90, 'energy': 0.25},
        'nervosismo': {'valence': -0.55, 'energy': 0.70},
        'otimismo': {'valence': 0.70, 'energy': 0.35},
        'orgulho': {'valence': 0.65, 'energy': 0.45},
        'realização': {'valence': 0.75, 'energy': 0.25},
        'alívio': {'valence': 0.60, 'energy': -0.55},
        'remorso': {'valence': -0.75, 'energy': -0.45},
        'tristeza': {'valence': -0.80, 'energy': -0.65},
        'surpresa': {'valence': 0.00, 'energy': 0.75},
        'neutro': {'valence': 0.00, 'energy': 0.00},
    }

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
