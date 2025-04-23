import requests


class AuthError(Exception):
    """
    Custom authentication error exception
    """

    def __init__(self, message):
        self.message = message
        self.error_code = 401
        super().__init__(self.message)


class User:
    def __init__(self):
        self.spotify_obj = {}
        self.is_loaded = False

    def load_spotify(
        self, access_token: str, limit: int = 10, time_range: str = "short_term"
    ) -> None:
        """
        Call Spotify API to load user spotify_obj object if it is not already loaded.
        """
        if self.is_loaded:
            return

        # every API call needs an "Authorization: Bearer TOKEN" in the header, so we declare it here
        headers = {"Authorization": f"Bearer {access_token}"}

        # load user info
        user_info_response = requests.get(
            "https://api.spotify.com/v1/me", headers=headers
        )
        if not user_info_response.ok:
            status = user_info_response.status_code
            raise (
                AuthError("The access token expired")
                if status == 401
                else Exception("Error making request")
            )

        # load top tracks
        params = {"limit": limit, "time_range": time_range}
        tracks_response = requests.get(
            "https://api.spotify.com/v1/me/top/tracks?", params=params, headers=headers
        )
        if not tracks_response.ok:
            status = tracks_response.status_code
            raise (
                AuthError("The access token expired")
                if status == 401
                else Exception("Error making request")
            )

        # set spotify_obj after all requests were successful
        self.spotify_obj["displayName"] = user_info_response.json().get("display_name")
        tracklist = []
        for track_object in tracks_response.json().get("items"):
            tracklist.append(
                {
                    "name": track_object.get("name"),
                    "artists": [artist.get("name") for artist in track_object.get("artists")],
                    "duration_s": track_object.get("duration_ms") // 1000,
                    "url": track_object.get("external_urls").get("spotify")
                }
            )
        self.spotify_obj["tracklist"] = tracklist
        self.is_loaded = True