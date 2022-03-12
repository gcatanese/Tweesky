import unittest

from tweesky.parser.spotify_parser import SpotifyTrack, SpotifyArtist, SpotifyPlaylist, SpotifyShow, SpotifyEpisode, \
    SpotifyAlbum, convert_to_hashtags, extract_year, format_duration, format_date, format_json_date, format_followers


class SpotifyParserTest(unittest.TestCase):

    def test_get_track(self):
        urn = 'https://open.spotify.com/track/346QlB0ow8uYiJ0KG9kftX?si=2ea01e0b84df42c7'
        track = SpotifyTrack(urn)

        self.assertIsNotNone(track)
        self.assertIsNotNone(track.track)

    def test_get_artist(self):
        urn = 'spotify:artist:4c1x5q3SgjyzgivpDvKF97'
        artist = SpotifyArtist(urn)

        self.assertIsNotNone(artist)
        self.assertIsNotNone(artist.artist)

    def test_get_playlist(self):
        urn = 'https://open.spotify.com/playlist/01vuO5VIsZlkVnCUAHno73?si=e78e4034be8341f8'
        playlist = SpotifyPlaylist(urn)

        self.assertIsNotNone(playlist)
        self.assertIsNotNone(playlist.playlist)

    def test_get_show(self):
        urn = 'https://open.spotify.com/show/1VXcH8QHkjRcTCEd88U3ti?si=JKG4lvjIRvuDgyNt4_1xgA'
        show = SpotifyShow(urn)

        self.assertIsNotNone(show)
        self.assertIsNotNone(show.show)

    def test_get_episode(self):
        urn = 'https://open.spotify.com/episode/2Tnc0cycgw1XtKkgbMLiFU?si=g1ZZivlJQcubiVL-lK2F3Q&nd=1'
        episode = SpotifyEpisode(urn)

        self.assertIsNotNone(episode)
        self.assertIsNotNone(episode.episode)

    def test_get_album(self):
        urn = 'spotify:album:0QzS84Cj8JXx1E0MsfMSqb'
        album = SpotifyAlbum(urn)

        self.assertIsNotNone(album)
        self.assertIsNotNone(album.album)

    def test_get_card(self):
        urn = 'https://open.spotify.com/track/346QlB0ow8uYiJ0KG9kftX?si=2ea01e0b84df42c7'

        parser = SpotifyTrack(urn)
        card = parser.get_card()

        self.assertEqual(card.twitter_card, 'summary_large_image')

    def test_format_duration(self):
        self.assertEqual(format_duration(249386), '4:09')

    def test_extract_year_from_yyyymmdd(self):
        self.assertEqual(extract_year('2021-02-18'), '2021')

    def test_extract_year_from_yyyymm(self):
        self.assertEqual(extract_year('2021-02'), '2021')

    def test_format_date(self):
        self.assertEqual(format_date('2021-03-29'), '29 Mar 2021')

    def test_format_json_date(self):
        self.assertEqual('29 Mar 2021', format_json_date('2021-03-29T20:44:50Z'))

    def test_convert_to_hashtags(self):
        self.assertEqual(convert_to_hashtags(['rock', 'trance']), '#rock #trance')

    def test_convert_to_hashtags_including_spaces(self):
        self.assertEqual(convert_to_hashtags(['new rock', 'best trance']), '#newrock #besttrance')

    def test_convert_to_hashtags_none(self):
        self.assertEqual(convert_to_hashtags(None), '')

    def test_convert_to_hashtags_empty_list(self):
        self.assertEqual(convert_to_hashtags([]), '')

    def test_format_followers(self):
        self.assertEqual('150,128', format_followers(150128))
