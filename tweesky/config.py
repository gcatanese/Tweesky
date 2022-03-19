import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def get_spotify_client_id():
    return os.environ.get("SPOTIFY_CLIENT_ID", None)


def get_spotify_client_secret():
    return os.environ.get("SPOTIFY_CLIENT_SECRET", None)


def get_screenshots_location():
    return os.environ.get("SCREENSHOTS_LOCATION", "/tmp")
