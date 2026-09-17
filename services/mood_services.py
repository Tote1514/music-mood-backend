from math import isfinite
from pathlib import Path

from transformers import BertForSequenceClassification, BertTokenizer, pipeline


class MoodGenerator:
    def __init__(self, threshold=0.1):
        '''
        Initialize the MoodGenerator with the specified model path and threshold.
        '''
        base_dir = Path(__file__).resolve().parent
        self.model_path = base_dir.parent / "nlp_models" / "fine_tuned_large_model"
        self.threshold = threshold

        self.model = BertForSequenceClassification.from_pretrained(self.model_path)
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)

        self.nlp = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            top_k=2
        )

    def process_texts(self, texts: list[str]):
        '''
        Process the input text to detect emotions and map them to moods.
        '''
        emotions = self.detect_emotions(texts)

        results = []
        for emotion in emotions:
            moods = self.map_emotions_to_moods(emotion)
            dominant = max(moods, key=lambda x: x["score"])["label"]

            results.append({
                "moods": moods,
                "dominant_mood": dominant
            })

        return results

    def process_texts_with_individual_emotions(self, texts: list[str]):
        """Return the two highest-scoring emotions, normalized to sum to one.

        Preserve original labels for EmotionMoodMapper. Unlike process_texts,
        this flow neither groups emotions nor applies the category threshold.
        The response keys remain compatible with MoodAnalysisResponse.
        """
        if not texts:
            return []

        results = []
        for emotions in self.detect_emotions(texts):
            normalized = self.normalize_top_emotions(emotions)
            results.append({
                'moods': normalized,
                'dominant_mood': normalized[0]['label'],
            })
        return results

    @staticmethod
    def normalize_top_emotions(emotions: list[dict]) -> list[dict]:
        """Select top-2 before normalization, without mutating predictions."""
        if not emotions:
            raise ValueError('No emotions provided')
        if any(
            not isfinite(emotion['score']) or not 0 <= emotion['score'] <= 1
            for emotion in emotions
        ):
            raise ValueError('Emotion scores must be finite and within [0, 1]')

        top_two = sorted(
            emotions, key=lambda emotion: emotion['score'], reverse=True,
        )[:2]
        total = sum(emotion['score'] for emotion in top_two)
        if total == 0:
            raise ValueError('Total emotion score cannot be zero')

        return [
            {'label': emotion['label'], 'score': emotion['score'] / total}
            for emotion in top_two
        ]

    def detect_emotions(self, texts: list[str]):
        ''' 
        Detect the most probable emotions in the input text.
        '''
        emotions = self.nlp(texts)
        return emotions

    def map_emotions_to_moods(self, emotions: list[dict]):
        '''
        Map detected emotions to broader mood categories.
        The mood categories are:
        - animado
        - triste
        - calmo
        - romantico
        - pesado
        '''
        mood_mapping = {
            ("alegria", "entusiasmo", "diversão", "otimismo",
             "aprovação", "orgulho", "realização", "surpresa"): "animado",
            ("tristeza", "decepção", "luto", "remorso"): "triste",
            ("neutro", "percepção", "alívio", "curiosidade",
             "nervosismo", "constrangimento", "confusão", "desejo"): "calmo",
            ("amor", "gratidão", "zelo", "admiração"): "romantico",
            ("raiva", "desaprovação", "aborrecimento",
             "nojo", "medo"): "pesado"
        }

        mood_scores = {}

        for emotion in emotions:
            label = emotion["label"]
            score = emotion["score"]

            # aplica threshold
            if score < self.threshold:
                continue

            for labels, mood in mood_mapping.items():
                if label in labels:
                    mood_scores[mood] = mood_scores.get(mood, 0) + score

        total = sum(mood_scores.values())
        if total > 0:
            mood_scores = {
                mood: score / total
                for mood, score in mood_scores.items()
            }

        return [
            {"label": mood, "score": score}
            for mood, score in mood_scores.items()
        ]
