import spotipy
import datetime, logging, json
import abc
from spotipy.oauth2 import SpotifyClientCredentials

from config import get_spotify_client_id, get_spotify_client_secret
from model.card import Card


class SpotifyParser:
    "Parser of Spotify URLs (tracks, artists, albums, etc.."

    def __init__(self, url=None):
        self.url = url
        self.sp_app = self.init_spotify()

        self.fetch()

    def init_spotify(self):
        if get_spotify_client_id() is None:
            raise Exception("Spotify Client Id not found")

        if get_spotify_client_secret() is None:
            raise Exception("Spotify Client Secret not found")

        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=get_spotify_client_id(),
                                                                     client_secret=get_spotify_client_secret()))

    @abc.abstractmethod
    def fetch(self):
        pass

    @abc.abstractmethod
    def find_title(self):
        pass

    @abc.abstractmethod
    def find_image(self):
        pass

    @abc.abstractmethod
    def find_description(self):
        pass

    def get_track(self, url):
        return self.sp_app.track(url)

    def get_artist(self, url):
        return self.sp_app.artist(url)

    def get_album(self, url):
        return self.sp_app.album(url)

    def get_show(self, url):
        return self.sp_app.show(url, market='US')

    def get_episode(self, url):
        return self.sp_app.episode(url, market='US')

    def get_playlist(self, url):
        return self.sp_app.playlist(url)

    def get_card(self):

        card = Card()
        card.url = self.url

        card.twitter_card = 'summary_large_image'
        card.title = self.find_title()
        card.description = self.find_description()
        card.image = self.find_image()

        return card

    def find_duration(self):
        duration_ms = self.track['duration_ms']

        return self.format_duration(duration_ms)

    def format_duration(self, duration_ms):

        if duration_ms is None:
            return None

        duration_ms = duration_ms / 1000
        min, sec = divmod(duration_ms, 60)

        min = int(min)
        sec = int(sec)
        sec = f'{sec:02}'  # pad with zero (if necessary)

        logging.info(f'{min}:{sec}')

        return f'{min}:{sec}'

    def format_followers(self, num_followers):
        return f'{num_followers:,}'

    def find_album(self):
        album = self.track['album']
        if album is not None:
            album_name = album['name']

        return album_name

    def find_album_release_date(self):
        return self.track['album']['release_date']

    def extract_year(self, release_date):
        year = None

        if release_date is not None:
            x = release_date.split("-")
            year = x[0]

        return year

    def format_date(self, date_spotify_format):
        return datetime.datetime.strptime(date_spotify_format, '%Y-%m-%d').strftime('%d %b %Y')

    def format_json_date(self, date_json_format):
        date_time_obj = datetime.datetime.strptime(date_json_format, '%Y-%m-%dT%H:%M:%SZ')

        return date_time_obj.strftime('%d %b %Y')

    def convert_to_hashtags(self, list):
        new_list = []

        if list is None:
            return ''

        for item in list:
            new_list.append(f'#{item.replace(" ", "")}')

        return ' '.join(new_list)

    def print_json(self, dict):
        return json.dumps(dict)


class SpotifyTrack(SpotifyParser):

    def fetch(self):
        """
        Fetch from URL
        :param url:
        :param token:
        :return:
        """
        self.track = self.get_track(self.url)
        artist_url = self.track['artists'][0]['uri']
        self.artist = self.get_artist(artist_url)

        logging.info(f'track: {self.print_json(self.track)}')
        logging.info(f'artist: {self.print_json(self.artist)}')

    def find_title(self):
        title = self.track['name']
        artist = self.artist['name']
        artist_followers = self.format_followers(self.artist['followers']['total'])

        return f"Play '{title}' by {artist} ({artist_followers} followers)"

    def find_description(self):
        title = self.track['name']
        album = self.find_album()
        total_tracks = self.track['album']['total_tracks']
        artist_homepage = self.track['artists'][0]['external_urls']['spotify']
        duration = self.find_duration()
        genres = self.artist['genres']
        album_release_date = self.extract_year(self.find_album_release_date())

        description = f'\'{title}\' is out of \'{album}\', released in {album_release_date} ' \
                      f'and including {total_tracks} track(s). {self.convert_to_hashtags(genres)}'

        return description

    def find_image(self):
        image = self.track['album']['images'][0]['url']
        return image


class SpotifyArtist(SpotifyParser):

    def fetch(self):
        """
        Fetch from URL
        :param url:
        :param token:
        :return:
        """

        self.artist = self.get_artist(self.url)

        logging.info(f'artist: {self.print_json(self.artist)}')

    def find_title(self):
        artist_name = self.artist['name']
        artist_followers = self.format_followers(self.artist['followers']['total'])

        return f"View {artist_name} ({artist_followers} followers)"

    def find_description(self):
        artist_homepage = self.artist['external_urls']['spotify']
        genres = self.artist['genres']

        description = f'Check out artist\'s home page {artist_homepage}. {self.convert_to_hashtags(genres)}'

        return description

    def find_image(self):
        image = self.artist['images'][0]['url']
        return image


class SpotifyAlbum(SpotifyParser):

    def fetch(self):
        """
        Fetch from URL
        :param url:
        :param token:
        :return:
        """

        self.album = self.get_album(self.url)

        logging.info(f'album: {self.print_json(self.album)}')

    def find_title(self):
        album_name = self.album['name']
        artist_url = self.album['artists'][0]['uri']
        self.artist = self.get_artist(artist_url)
        artist_name = self.artist['name']
        artist_followers = self.format_followers(self.artist['followers']['total'])

        return f"Play \'{album_name} by {artist_name} ({artist_followers} followers)"

    def find_description(self):
        artist_homepage = self.artist['external_urls']['spotify']
        album_name = self.album['name']
        total_tracks = self.album['total_tracks']
        album_release_date = self.extract_year(self.album['release_date'])

        genres = self.artist['genres']

        description = f'\'{album_name}\' has been released in {album_release_date} and it includes {total_tracks} track(s) ' \
                      f'{self.convert_to_hashtags(genres)}'

        return description

    def find_image(self):
        image = self.album['images'][0]['url']
        return image


class SpotifyShow(SpotifyParser):

    def fetch(self):
        """
        Fetch from URL
        :param url:
        :param token:
        :return:
        """

        self.show = self.get_show(self.url)

        logging.info(f'show: {self.print_json(self.show)}')

    def find_title(self):
        show_name = self.show['name']
        publisher = self.show['publisher']
        total_episodes = self.show['total_episodes']
        languages = self.show['languages']

        last_episode_release_date = self.show['episodes']['items'][0]['release_date']
        last_episode_title = self.show['episodes']['items'][0]['name']

        return f"Listen to \'{show_name}\' by {publisher} (last episode on {self.format_date(last_episode_release_date)}) "

    def find_description(self):
        show_description = self.show['description']

        description = show_description

        return description

    def find_image(self):
        image = self.show['images'][0]['url']
        return image


class SpotifyEpisode(SpotifyParser):

    def fetch(self):
        """
        Fetch from URL
        :param url:
        :param token:
        :return:
        """

        self.episode = self.get_episode(self.url)

        logging.info(f'episode: {self.print_json(self.episode)}')

    def find_title(self):
        episode_name = self.episode['name']
        publisher = self.episode['show']['publisher']

        episode_release_date = self.episode['release_date']

        return f"Listen to \'{episode_name}\' by {publisher} (published on {self.format_date(episode_release_date)})"

    def find_description(self):
        episode_description = self.episode['description']

        description = episode_description

        return description

    def find_image(self):
        image = self.episode['images'][0]['url']
        return image


class SpotifyPlaylist(SpotifyParser):

    def fetch(self):
        """
        Fetch from URL
        :param url:
        :param token:
        :return:
        """

        self.playlist = self.get_playlist(self.url)

        logging.info(f'playlist: {self.print_json(self.playlist)}')

    def find_title(self):
        playlist_name = self.playlist['name']
        owner = self.playlist['owner']['display_name']
        followers = self.playlist['followers']['total']

        if followers == 1:
            str_followers = '1 follower'
        else:
            str_followers = f'{self.format_followers(followers)} followers'

        return f"Listen to \'{playlist_name}\' by {owner} ({str_followers}) "

    def find_description(self):
        playlist_description = self.playlist['description']

        tracks = self.playlist['tracks']['items']

        last_added_date = None
        for track in tracks:
            if last_added_date is None or track['added_at'] > last_added_date:
                last_added_date = track['added_at']

        return f'The playlist includes {self.find_num_tracks()} tracks and it was last updated on ' \
               f'{self.format_json_date(last_added_date)}'

    def find_image(self):
        image = self.playlist['images'][0]['url']
        return image

    def find_num_tracks(self):
        num_tracks = str(self.playlist['tracks']['total'])
        return num_tracks
