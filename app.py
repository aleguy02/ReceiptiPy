import requests
from flask import Flask, request, redirect, session, url_for, render_template, jsonify
from urllib import parse

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
    permissions_scope = "user-top-read"
    query_params = {
        "response_type": "code",
        "client_id": Config.CLIENT_ID,
        "scope": permissions_scope,
        "redirect_uri": Config.REDIRECT_URI,
    }
    auth_url = "https://accounts.spotify.com/authorize?" + parse.urlencode(query_params)
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

        auth_header = generate_auth_header()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            "https://accounts.spotify.com/api/token", data=payload, headers=headers
        ).json()
        if not response or not response.get("access_token"):
            raise Exception("Spotify API Response not found")
        access_token = response["access_token"]
        session["access_token"] = access_token

        return redirect(url_for("home"))
    except Exception as e:
        return f"<h1>Exception occurred</h1><p>{str(e)}<p>"


@app.route("/haikus", methods=["GET"])
def home():
    if "access_token" not in session:
        return redirect(url_for("login_to_spotify"))
    return render_template("index.html", user=user)


@app.route("/api/makehaiku", methods=["POST"])
def generate_haiku():
    """
    Generate a haiku from the lyrics of the user's top track
    """
    try:
        user.load_spotify(session["access_token"])
        # response = user.generate_haiku()
    except AuthError as e:
        session.pop("access_token", None)
        return redirect(url_for("index"))
    except Exception as e:
        return f"<h1>Exception occurred</h1><p>{str(e)}<p>"

    return "Hello world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
