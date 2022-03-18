import unittest

from tweesky.main import generate_card, generate_card_as_html, generate_card_as_json


class MainTest(unittest.TestCase):

    def test_generate_card(self):
        url = 'https://perosa.github.io/'
        card = generate_card(url)

        self.assertIsNotNone(card)
        self.assertEqual('Perosa', card.title)
        self.assertEqual(url, card.url)

    # def test_generate_card_with_screenshot(self):
    #     url = 'https://www.frenkiedejong.com/'
    #     card = generate_card(url)
    #
    #     self.assertIsNotNone(card)
    #     self.assertEqual(url, card.url)
    #     self.assertTrue(card.image.startswith("file://"))

    def test_generate_card_as_html(self):
        url = 'https://perosa.github.io/'
        html_card = generate_card_as_html(url)

        self.assertIsNotNone(html_card)

    def test_generate_card_as_json(self):
        url = 'https://perosa.github.io/'
        json_card = generate_card_as_json(url)

        self.assertIsNotNone(json_card)

    def test_generate_card_from_spotify_url(self):
        url = 'https://open.spotify.com/track/346QlB0ow8uYiJ0KG9kftX?si=2ea01e0b84df42c7'
        card = generate_card(url=url)

        self.assertIsNotNone(card)
        self.assertIsNotNone(card.title)
        self.assertEqual(url, card.url)
