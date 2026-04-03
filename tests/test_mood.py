from unittest.mock import Mock, patch

import pytest

from services.mood_services import MoodGenerator


@pytest.fixture
def mood_generator():
    with patch('services.mood_services.BertForSequenceClassification.from_pretrained'), \
         patch('services.mood_services.BertTokenizer.from_pretrained'), \
         patch('services.mood_services.pipeline'):
        generator = MoodGenerator(threshold=0.1)
        return generator


def test_process_texts_single_text(mood_generator):
    mock_emotions = [
        [
            {"label": "alegria", "score": 0.8},
            {"label": "entusiasmo", "score": 0.7}
        ]
    ]
    mood_generator.detect_emotions = Mock(return_value=mock_emotions)

    result = mood_generator.process_texts(["I am very happy"])

    assert len(result) == 1
    assert result[0]["dominant_mood"] == "animado"
    assert len(result[0]["moods"]) > 0


def test_process_texts_multiple_texts(mood_generator):
    mock_emotions = [
        [{"label": "alegria", "score": 0.9}],
        [{"label": "tristeza", "score": 0.85}]
    ]
    mood_generator.detect_emotions = Mock(return_value=mock_emotions)

    result = mood_generator.process_texts(["Happy text", "Sad text"])

    assert len(result) == 2
    assert result[0]["dominant_mood"] == "animado"
    assert result[1]["dominant_mood"] == "triste"


def test_process_texts_empty_list(mood_generator):
    mock_emotions = []
    mood_generator.detect_emotions = Mock(return_value=mock_emotions)

    result = mood_generator.process_texts([])

    assert result == []


def test_process_texts_below_threshold(mood_generator):
    mock_emotions = [
        [
            {"label": "amor", "score": 0.05},
            {"label": "remorso", "score": 0.2}
        ]
    ]

    mood_generator.detect_emotions = Mock(return_value=mock_emotions)

    result = mood_generator.process_texts(["Some text"])

    assert len(result) == 1

    moods = result[0]["moods"]

    assert len(moods) == 1
    assert moods[0]["label"] == "triste"
    assert moods[0]["score"] == 1


def test_process_texts_mixed_emotions(mood_generator):
    mock_emotions = [
        [
            {"label": "raiva", "score": 0.6},
            {"label": "nojo", "score": 0.5}
        ]
    ]
    mood_generator.detect_emotions = Mock(return_value=mock_emotions)

    result = mood_generator.process_texts(["Angry text"])

    assert len(result) == 1
    assert result[0]["dominant_mood"] == "pesado"
