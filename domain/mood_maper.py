from typing import List, Dict, Tuple


class MoodMapper:
    MOOD_PROFILE = {
        "animado": {
            "energy": 0.9,
            "valence": 0.8,
            "danceability": 0.7,
            "mode": 1
        },
        "triste": {
            "energy": 0.2,
            "valence": 0.2,
            "danceability": 0.3,
            "mode": 0
        },
        "calmo": {
            "energy": 0.3,
            "valence": 0.5,
            "danceability": 0.2,
            "mode": 1
        },
        "romantico": {
            "energy": 0.4,
            "valence": 0.7,
            "danceability": 0.5,
            "mode": 1
        },
        "pesado": {
            "energy": 0.9,
            "valence": 0.3,
            "danceability": 0.4,
            "mode": 0
        }
    }

    def map(self, moods: List) -> Dict:
        # filtra moods válidos
        valid_moods = [m for m in moods if m.label in self.MOOD_PROFILE]

        if not valid_moods:
            raise ValueError("No valid moods provided")

        total_score = sum(m.score for m in valid_moods)

        # evita divisão por zero
        if total_score == 0:
            raise ValueError("Total mood score cannot be zero")

        # 🎧 cálculo das features contínuas
        energy = sum(
            m.score * self.MOOD_PROFILE[m.label]["energy"]
            for m in valid_moods
        ) / total_score

        valence = sum(
            m.score * self.MOOD_PROFILE[m.label]["valence"]
            for m in valid_moods
        ) / total_score

        danceability = sum(
            m.score * self.MOOD_PROFILE[m.label]["danceability"]
            for m in valid_moods
        ) / total_score

        # 🎼 mode (binário)
        mode_value = sum(
            m.score * self.MOOD_PROFILE[m.label]["mode"]
            for m in valid_moods
        ) / total_score

        mode = 1 if mode_value >= 0.5 else 0

        # 🎯 tolerância dinâmica (quanto mais mistura, maior a tolerância)
        max_score = max(m.score for m in valid_moods)
        diversidade = 1 - max_score  # 0 = dominante, 1 = bem distribuído

        tolerance = 0.1 + (0.2 * diversidade)

        # 🔒 clamp para manter valores entre 0 e 1
        def clamp(value: float) -> float:
            return max(0.0, min(1.0, value))

        filters = {
            "energy": (
                clamp(energy - tolerance),
                clamp(energy + tolerance)
            ),
            "valence": (
                clamp(valence - tolerance),
                clamp(valence + tolerance)
            ),
            "danceability": (
                clamp(danceability - tolerance),
                clamp(danceability + tolerance)
            ),
            "mode": mode
        }

        return filters