from src.parser.http_parser import HttpParser
from src.parser.spotify_parser import SpotifyParser


def get_parser(url):
    if 'open.spotify.com' in url:
        return SpotifyParser(url)
    else:
        return HttpParser(url)