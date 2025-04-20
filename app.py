import requests
from flask import Flask, request, redirect, session, url_for
from urllib import parse
import base64

# from src.utils import generate_random_string
from src.utils import generate_auth_header
from src.config.config import Config
from src.user.user import User


user = User()
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY


@app.route("/", methods=["GET"])
def index():
    if "access_token" not in session:
        return redirect(url_for("login_to_spotify"))
    return redirect(url_for("home"))


@app.route("/login", methods=["GET"])
def login_to_spotify():
    # For securing our request/response
    # state: str = generate_random_string(10)

    # Spotify permissions scopes
    permissions_scope: str = "user-top-read"
    query_params: dict = {
        "response_type": "code",
        "client_id": Config.CLIENT_ID,
        "scope": permissions_scope,
        "redirect_uri": Config.REDIRECT_URI,
        # "state": state,
    }
    auth_url: str = "https://accounts.spotify.com/authorize?" + parse.urlencode(
        query_params
    )
    return redirect(auth_url)


@app.route("/callback", methods=["GET", "POST"])
def exchange_auth_code_for_access_token():
    try:
        # auth_code, state = request.args.get("code"), request.args.get("state")
        auth_code: str = request.args.get("code")
        payload: dict = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": Config.REDIRECT_URI,
        }

        # Make sure to decode the b64 encoded value to pass a string instead of bytes to Authorization
        auth_header: str = generate_auth_header()
        headers: dict = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        post_request = requests.post(
            "https://accounts.spotify.com/api/token", data=payload, headers=headers
        )
        response: dict = post_request.json()
        if not response or not response["access_token"]:
            raise Exception("Spotify API Response not found")
        access_token: str = response["access_token"]
        session["access_token"] = access_token

        return redirect(url_for("home"))
    except Exception as e:
        return f"<h1>Exception occurred</h1><p>{str(e)}<p>"


@app.route("/haikus", methods=["GET", "POST"])
def home():
    if "access_token" not in session:
        return redirect(url_for("login_to_spotify"))

    return f"<p>User message: {user.message}</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
