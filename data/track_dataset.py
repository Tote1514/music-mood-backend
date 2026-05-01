from typing import List

import pandas as pd


class TrackDataset:
    def __init__(self, csv_file):
        try:
            self.data = pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"Error: The file '{csv_file}' was not found.")
            self.data = pd.DataFrame()  # Create an empty DataFrame to avoid further errors

    def filter(self, genres: List[str], features, n_tracks=10):
        df = self.get_data()
        df = self.filter_by_genres(df, genres)
        df = self.filter_by_features(df, features)
        df = self.get_n_random_tracks(df, n_tracks)
        return df

    def __len__(self):
        return len(self.data)

    def get_data(self):
        return self.data

    def filter_by_genres(self, df, genres: List[str]):
        if df.empty:
            print("Warning: No data available to filter.")
            return pd.DataFrame()
        return df[df['track_genre'].isin(genres)]

    def filter_by_features(self, df, features):
        if df.empty:
            print("Warning: No data available to filter.")
            return pd.DataFrame()
        # some filtering logic based on features
        return df

    def get_n_random_tracks(self, df, n=10):
        if df.empty:
            print("Warning: No data available to sample.")
            return pd.DataFrame()
        return df.sample(n)

    def get_ids(self, df):
        if df.empty:
            print("Warning: No data available to extract IDs.")
            return []
        return df['track_id'].tolist()
