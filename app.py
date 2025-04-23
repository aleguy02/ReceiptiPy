import requests
from flask import Flask, request, redirect, session, url_for, render_template, jsonify
from urllib import parse
from datetime import date

# from src.utils import generate_random_string
from src.utils import generate_auth_header
from src.config.config import Config
from src.user.user import User, AuthError

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
    """
    Log user into Spotify
    """
    # Spotify permissions scopes
    permissions_scope = "user-top-read user-read-private user-read-email"
    auth_url = "https://accounts.spotify.com/authorize?" + parse.urlencode(
        {
            "response_type": "code",
            "client_id": Config.CLIENT_ID,
            "scope": permissions_scope,
            "redirect_uri": Config.REDIRECT_URI,
        }
    )
    return redirect(auth_url)


@app.route("/callback", methods=["GET", "POST"])
def exchange():
    """
    Exchanges Spotify authorization code for access token
    """
    try:
        auth_code = request.args.get("code")
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": Config.REDIRECT_URI,
        }
        headers = {
            "Authorization": f"Basic {generate_auth_header()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            "https://accounts.spotify.com/api/token", data=payload, headers=headers
        ).json()
        if not response or not response.get("access_token"):
            raise Exception("Spotify API Response not found")
        session["access_token"] = response["access_token"]

        return redirect(url_for("home"))
    except Exception as e:
        return f"<h1>Exception occurred</h1><p>{str(e)}<p>"


dummy_data = {
    "username": "aleguy02",
    "tracklist": [
        {"name": "Denver", "artist": "Jack Harlow"},
        {"name": "Hurts Me", "artist": "Tory Lanez"},
    ],
}


@app.route("/receipt", methods=["GET"])
def home():
    if "access_token" not in session:
        return redirect(url_for("login_to_spotify"))

    try:
        user.load_spotify(session["access_token"])
        today = date.today().strftime("%a, %B %d, %Y")
    except AuthError as e:
        session.pop("access_token", None)
        return redirect(url_for("index"))
    return render_template("index.html", user=user.spotify_obj, fdate=today)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
