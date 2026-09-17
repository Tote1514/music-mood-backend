from data.track_dataset import TrackDataset
from domain.mood_mapper_strategy import MoodMapperStrategy
from services.spotify_services import spotify


class RecommendationService:
    def __init__(
        self,
        dataset: TrackDataset,
        mood_mapper: MoodMapperStrategy,
        access_token: str,
    ):
        self.dataset = dataset
        self.mood_mapper = mood_mapper
        self.access_token = access_token

    async def recommend(self, genres, moods, n_tracks=5):
        id_list = self.get_filtered_track_ids(genres, moods, n_tracks)
        tracks_details = await self.get_track_details(id_list)
        tracks = self.process_tracks(tracks_details)
        return {"tracks": tracks}

    def get_filtered_track_ids(self, genres, moods, n_tracks):
        features = self.mood_mapper.map(moods)
        df = self.dataset.filter(genres, features=features, n_tracks=n_tracks)
        id_list = self.dataset.get_ids(df)
        return id_list

    async def get_track_details(self, track_ids):
        if not track_ids:
            return []

        try:
            tracks_details = await spotify.get_tracks_info(
                self.access_token,
                track_ids,
            )
            return tracks_details
        except Exception as e:
            print(f"Error fetching track details: {e}")
            return []

    @staticmethod
    def process_tracks(track_details):
        processed_tracks = []
        for track in track_details:
            if not track:
                continue

            album = track.get("album") or {}
            album_images = album.get("images") or []
            album_cover_url = (
                album_images[0].get("url") if album_images else None
            )
            processed_tracks.append({
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album_cover_url": album_cover_url,
                "spotify_url": track["external_urls"]["spotify"],
                "uri": track["uri"]
            })
        return processed_tracks
