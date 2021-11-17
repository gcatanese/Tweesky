from src.parser.html_parser import HtmlParser
from src.parser.spotify_parser import SpotifyParser


def get_parser(url=None, html=None):
    if 'open.spotify.com' in url:
        return SpotifyParser(url)
    else:
        return HtmlParser(url, html)