import os
from dotenv import load_dotenv
from flask import Flask, request, redirect
from urllib.parse import urlencode

from src.utils import generate_random_string

load_dotenv()

client_id: str = os.getenv("CLIENT_ID")
redirect_uri: str = "http://127.0.0.1:5000/callback"

app = Flask(__name__)

# redirect depending on sign-in state
@app.route("/")
def redir():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login_to_spotify():
    # For securing our request/response
    state: str = generate_random_string(10)

    # Spotify permissions scopes
    scope: str = "user-top-read"

    query_params: dict = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
        "state": state,
    }

    auth_url: str = "https://accounts.spotify.com/authorize?" + urlencode(query_params)
    return redirect(auth_url)


# @app.route("/haiku")
# def generate_haiku():
#     pass



if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)