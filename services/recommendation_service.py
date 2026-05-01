from data.track_dataset import TrackDataset


class RecommendationService:
    def __init__(self, dataset: TrackDataset, mood_mapper):
        self.dataset = dataset
        self.mood_mapper = mood_mapper

    def recommend(self, genres, moods, n_tracks=10):
        features = self.mood_mapper.map(moods)
        df = self.dataset.filter(genres, features, n_tracks)
        id_list = self.dataset.get_ids(df)
        return df
