"""Common contract for converting scored labels into emotional coordinates."""

from abc import ABC, abstractmethod
from typing import Dict, List

from schemas.mood_schema import Mood


class MoodMapperStrategy(ABC):
    @abstractmethod
    def map(self, moods: List[Mood]) -> Dict[str, float]:
        """Return energy and valence in [-1, 1] for supported labels.

        Implementations ignore unsupported labels and reject inputs with no
        supported labels or with a zero total score.
        """
        raise NotImplementedError
