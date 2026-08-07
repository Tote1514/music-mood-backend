from data.track_dataset import TrackDataset
from services.spotify_services import spotify


class RecommendationService:
    def __init__(self, dataset: TrackDataset, mood_mapper, access_token: str):
        self.dataset = dataset
        self.mood_mapper = mood_mapper
        self.access_token = access_token

    async def recommend(self, genres, moods, n_tracks=10):
        id_list = self.get_filtered_track_ids(genres, moods, n_tracks)
        tracks_details = await self.get_track_details(id_list)
        tracks = self.process_tracks(tracks_details)
        return {"tracks": tracks}

    def get_filtered_track_ids(self, genres, moods, n_tracks):
        # features = self.mood_mapper.map(moods)
        df = self.dataset.filter(genres, features=None, n_tracks=n_tracks)
        id_list = self.dataset.get_ids(df)
        return id_list

    async def get_track_details(self, track_ids):
        try:
            tracks_details = await spotify.get_tracks_info(self.access_token, track_ids)
            return tracks_details
        except Exception as e:
            print(f"Error fetching track details: {e}")
            return []

    def process_tracks(self, track_details):
        processed_tracks = []
        for track in track_details:
            processed_tracks.append({
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album_cover_url": track["album"]["images"][0]["url"],
                "spotify_url": track["external_urls"]["spotify"],
                "uri": track["uri"]
            })
        return processed_tracks
