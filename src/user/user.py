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

    def load_spotify(
        self, access_token: str, limit: int = 1, time_range: str = "short_term"
    ) -> None:
        """
        Call Spotify API to load user spotify_obj object if it is not already loaded.
        """
        # avoid unnecessary api calls
        if self.spotify_obj.get("name") and self.spotify_obj.get("artist"):
            return

        params = {"limit": limit, "time_range": time_range}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://api.spotify.com/v1/me/top/tracks?", params=params, headers=headers
        )
        if not response.ok:
            if response.status_code == 401:
                raise AuthError("The access token expired")
            raise Exception("Error making request")

        self.spotify_obj["name"] = response.json().get("items")[0].get("name")
        self.spotify_obj["artist"] = (
            response.json().get("items")[0].get("artists")[0].get("name")
        )
