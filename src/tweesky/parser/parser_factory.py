import logging

from tweesky.parser.html_parser import HtmlParser
from tweesky.parser.spotify_parser import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyEpisode, SpotifyPlaylist, \
    SpotifyShow


def get_parser(url=None, html=None):
    if 'open.spotify.com' in url:
        return get_spotify_handler(url)
    else:
        return HtmlParser(url, html)


def get_spotify_handler(url):
    if 'open.spotify.com/album/' in url:
        return SpotifyAlbum(url)
    elif 'open.spotify.com/track/' in url:
        return SpotifyTrack(url)
    elif 'open.spotify.com/artist/' in url:
        return SpotifyArtist(url)
    elif 'open.spotify.com/show/' in url:
        return SpotifyShow(url)
    elif 'open.spotify.com/episode/' in url:
        return SpotifyEpisode(url)
    elif 'open.spotify.com/playlist/' in url:
        return SpotifyPlaylist(url)
    else:
        logging.error(f"Handler not found for {url}")
