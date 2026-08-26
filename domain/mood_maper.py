from typing import Dict, List


class MoodMapper:
    MOOD_PROFILE = {
        "animado": {
            "energy": 0.65,
            "valence": 0.70,
        },
        "triste": {
            "energy": -0.55,
            "valence": -0.70,
        },
        "calmo": {
            "energy": -0.65,
            "valence": 0.35,
        },
        "romantico": {
            "energy": -0.20,
            "valence": 0.55,
        },
        "pesado": {
            "energy": 0.75,
            "valence": -0.65,
        },
    }

    def map(self, moods: List) -> Dict:
        valid_moods = [m for m in moods if m.label in self.MOOD_PROFILE]

        if not valid_moods:
            raise ValueError("No valid moods provided")

        total_score = sum(m.score for m in valid_moods)

        if total_score == 0:
            raise ValueError("Total mood score cannot be zero")

        energy = sum(
            m.score * self.MOOD_PROFILE[m.label]["energy"]
            for m in valid_moods
        ) / total_score

        valence = sum(
            m.score * self.MOOD_PROFILE[m.label]["valence"]
            for m in valid_moods
        ) / total_score

        return {
            "energy": float(energy),
            "valence": float(valence),
        }
