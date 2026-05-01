from data.track_dataset import TrackDataset


def test_track_dataset_filter():
    dataset = TrackDataset('data/processed/spotify-tracks-filtered.csv')
    genres = ['rock', 'pop']
    features = {'energy': 0.8, 'valence': 0.7}
    filtered_df = dataset.filter(genres, features, n_tracks=5)
    assert not filtered_df.empty
    assert all(filtered_df['track_genre'].isin(genres))
    assert len(filtered_df) <= 5


def test_track_dataset_get_ids():
    dataset = TrackDataset('data/processed/spotify-tracks-filtered.csv')
    genres = ['rock']
    features = {'energy': 0.8, 'valence': 0.7}
    filtered_df = dataset.filter(genres, features, n_tracks=5)
    ids = dataset.get_ids(filtered_df)
    assert isinstance(ids, list)
