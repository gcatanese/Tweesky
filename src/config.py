import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def get_webdriver_path():
    return os.environ.get("WEBDRIVER_PATH", "./webdriver/chromedriver")


def get_webdriver_type():
    # returns webdriver to be used: remote | local
    return os.environ.get("WEBDRIVER_TYPE", "local")


def get_webdriver_remote_host():
    return os.environ.get("WEBDRIVER_REMOTE_HOST", "http://localhost:4444")


def get_spotify_client_id():
    return os.environ.get("SPOTIFY_CLIENT_ID", None)


def get_spotify_client_secret():
    return os.environ.get("SPOTIFY_CLIENT_SECRET", None)


def get_home_folder():
    return os.environ.get("HOME_LOCATION", "/tmp/")


def get_base_url():
    return os.environ.get("BASE_URL", "http://localhost:5000") + "/t"


def get_screenshots_location():
    return get_home_folder() + 'files/screenshots/'

