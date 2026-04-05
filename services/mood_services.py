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
            breakpoint()
            dominant = max(moods, key=lambda x: x["score"])["label"]

            results.append({
                "moods": moods,
                "dominant_mood": dominant
            })

        return results

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
