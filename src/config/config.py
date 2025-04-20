import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI")
    FLASK_SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY")
