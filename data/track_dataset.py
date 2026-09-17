import re
import unicodedata
from enum import Enum
from math import isfinite
from typing import List

import numpy as np
import pandas as pd


class FilterType(Enum):
    EUCLIDEAN = 1
    COSINE = 2


class TrackDataset:
    MIN_POPULARITY = 60
    CANDIDATE_POOL_SIZE = 50
    VERSION_SUFFIX_PATTERN = re.compile(
        r'\s*(?:[-\u2013\u2014]\s*|\()'
        r'(?:remaster(?:ed)?(?:\s+\d{4})?|single version|album version)'
        r'\)?\s*$',
        flags=re.IGNORECASE,
    )

    def __init__(self, csv_file):
        try:
            self.data = pd.read_csv(csv_file)
        except FileNotFoundError:
            print(f"Error: The file '{csv_file}' was not found.")
            self.data = pd.DataFrame()

    def filter(
        self,
        genres: List[str],
        features=None,
        n_tracks=5,
        filter_type: FilterType = FilterType.EUCLIDEAN,
    ):
        df = self.get_data()
        df = self.filter_by_genres(df, genres)
        df = self.filter_by_popularity(df)
        df = self.remove_duplicate_songs(df)
        df = self.filter_by_features(df, features, filter_type)
        df = self.get_random_tracks_from_top(
            df,
            n_tracks=n_tracks,
            pool_size=self.CANDIDATE_POOL_SIZE,
        )
        return df

    def __len__(self):
        return len(self.data)

    def get_data(self):
        return self.data

    @staticmethod
    def filter_by_genres(df, genres: List[str]):
        if df.empty:
            return pd.DataFrame()
        if not genres:
            return df.copy()
        return df[df['track_genre'].isin(genres)].copy()

    def filter_by_popularity(self, df):
        if df.empty:
            return pd.DataFrame()
        return df[df['popularity'] >= self.MIN_POPULARITY].copy()

    def remove_duplicate_songs(self, df):
        if df.empty:
            return pd.DataFrame()

        deduplicated_df = df.copy()
        deduplicated_df['_song_key'] = (
            deduplicated_df['artists'].map(self._normalize_text)
            + '|'
            + deduplicated_df['track_name'].map(
                self._normalize_track_name
            )
        )
        deduplicated_df = (
            deduplicated_df.sort_values(
                by=['popularity', 'track_id'],
                ascending=[False, True],
            )
            .drop_duplicates(subset='_song_key', keep='first')
            .drop(columns='_song_key')
        )
        return deduplicated_df

    @staticmethod
    def _normalize_text(value):
        normalized = unicodedata.normalize('NFKD', str(value))
        normalized = normalized.encode('ascii', 'ignore').decode()
        normalized = re.sub(r'[^a-z0-9]+', ' ', normalized.lower())
        return normalized.strip()

    def _normalize_track_name(self, value):
        without_version = self.VERSION_SUFFIX_PATTERN.sub('', str(value))
        return self._normalize_text(without_version)

    def filter_by_features(
        self,
        df,
        features,
        filter_type: FilterType = FilterType.EUCLIDEAN,
    ):
        if df.empty:
            print("Warning: No features to filter.")
            return pd.DataFrame()
        if features is None:
            return df.copy()
        if not isinstance(filter_type, FilterType):
            raise ValueError(f"Unsupported filter type: {filter_type}")

        energy, valence = self._validate_features(features)
        ranked_df = df.copy()

        if filter_type == FilterType.EUCLIDEAN:
            ranked_df['distance'] = self._euclidean_distance(
                ranked_df,
                energy,
                valence,
            )
        else:
            ranked_df['distance'] = self._cosine_distance(
                ranked_df,
                energy,
                valence,
            )

        return ranked_df.sort_values(
            by=['distance', 'popularity', 'track_id'],
            ascending=[True, False, True],
        )

    @staticmethod
    def _validate_features(features):
        try:
            energy = float(features['energy'])
            valence = float(features['valence'])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                "Features must contain numeric energy and valence values."
            ) from error

        if not isfinite(energy) or not isfinite(valence):
            raise ValueError("Energy and valence must be finite values.")

        return energy, valence

    @staticmethod
    def _euclidean_distance(df, energy, valence):
        return np.hypot(
            df['energy'] - energy,
            df['valence'] - valence,
        )

    def _cosine_distance(self, df, energy, valence):
        query_norm = np.hypot(energy, valence)
        if query_norm == 0:
            return self._euclidean_distance(df, energy, valence)

        track_norm = np.hypot(df['energy'], df['valence'])
        dot_product = df['energy'] * energy + df['valence'] * valence
        denominator = track_norm * query_norm
        cosine_similarity = np.divide(
            dot_product,
            denominator,
            out=np.zeros(len(df), dtype=float),
            where=denominator.to_numpy() != 0,
        )
        return 1 - np.clip(cosine_similarity, -1, 1)

    @staticmethod
    def get_random_tracks_from_top(df, n_tracks=5, pool_size=50):
        if not isinstance(n_tracks, int) or not isinstance(pool_size, int):
            raise TypeError("n_tracks and pool_size must be integers.")
        if n_tracks < 0 or pool_size < 0:
            raise ValueError("n_tracks and pool_size cannot be negative.")
        if df.empty:
            print("Warning: No data available to find nearest tracks.")
            return pd.DataFrame()

        candidate_pool = df.head(pool_size)
        sample_size = min(n_tracks, len(candidate_pool))
        sampled_tracks = candidate_pool.sample(n=sample_size)

        if 'distance' in sampled_tracks.columns:
            return sampled_tracks.sort_values(
                by=['distance', 'popularity', 'track_id'],
                ascending=[True, False, True],
            )
        return sampled_tracks

    @staticmethod
    def get_ids(df):
        if df.empty:
            print("Warning: No data available to extract IDs.")
            return []
        return df['track_id'].tolist()
