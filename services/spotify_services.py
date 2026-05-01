from http import HTTPStatus
from typing import List

import requests
from fastapi import HTTPException


class Spotify_Service:
    async def get_user_profile(self, access_token: str):
        user_info_url = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(user_info_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch user info from Spotify"
            )

        display_name = response.json().get("display_name", "User")

        return {"display_name": display_name}

    async def create_playlist(self, access_token: str,
                        playlist_name: str,
                        description: str,
                        track_uris: list):
        playlist = await self._create_playlist(access_token,
                                         playlist_name,
                                         description)
        await self._add_tracks_to_playlist(access_token, playlist["id"], track_uris)
        return {
            "id": playlist["id"],
            "name": playlist["name"],
            "url": playlist["external_urls"]["spotify"],
        }

    async def _create_playlist(self, access_token: str,
                         playlist_name: str,
                         description: str):
        create_playlist_url = "https://api.spotify.com/v1/me/playlists"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": playlist_name,
            "description": description,
            "public": False
        }

        response = requests.post(create_playlist_url,
                                 json=payload,
                                 headers=headers)
        if response.status_code != HTTPStatus.CREATED:
            raise HTTPException(status_code=response.status_code,
                                detail="Failed to create playlist on Spotify")

        return response.json()

    async def _add_tracks_to_playlist(self, access_token: str,
                                playlist_id: str,
                                track_uris: list):
        add_tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "uris": track_uris
        }

        response = requests.post(add_tracks_url,
                                json=payload,
                                headers=headers)
        if response.status_code != HTTPStatus.CREATED:
            raise HTTPException(status_code=response.status_code,
                        detail="Failed to add tracks to playlist on Spotify")

        return response.json()

    async def get_tracks_info(self, access_token: str, track_ids: List[str]):
        track_info_url = "https://api.spotify.com/v1/tracks"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "ids": ",".join(track_ids)
        }

        response = requests.get(track_info_url, headers=headers, params=params)

        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch track info from Spotify: {response.text}"
            )

        return response.json()["tracks"]

spotify = Spotify_Service()
