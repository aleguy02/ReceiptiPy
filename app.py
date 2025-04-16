import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, redirect
from urllib import parse
import base64

from src.utils import generate_random_string

load_dotenv()

CLIENT_ID: str = os.getenv("CLIENT_ID")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
REDIRECT_URI: str = os.getenv("REDIRECT_URI")

app = Flask(__name__)


# redirect depending on sign-in state
@app.route("/")
def redir():
    return "<p>Hello, World!</p>"


@app.route("/login")
def login_to_spotify():
    # For securing our request/response
    # state: str = generate_random_string(10)

    # Spotify permissions scopes
    permissions_scope: str = "user-top-read"
    query_params: dict = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": permissions_scope,
        "redirect_uri": REDIRECT_URI,
        # "state": state,
    }
    auth_url: str = "https://accounts.spotify.com/authorize?" + parse.urlencode(
        query_params
    )
    return redirect(auth_url)


@app.route("/callback", methods=["GET", "POST"])
def exchange_auth_code_for_access_token():
    # auth_code, state = request.args.get("code"), request.args.get("state")
    auth_code = request.args.get("code")
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    # Make sure to decode the b64 encoded value to pass a string instead of bytes to Authorization
    auth_header = base64.b64encode(
        (CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")
    ).decode()  # this article was helpful: https://ioflood.com/blog/python-base64-encode/
    print(auth_header)
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    post_request = requests.post(
        "https://accounts.spotify.com/api/token", data=payload, headers=headers
    )

    return f"<p>${post_request.text}<p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
