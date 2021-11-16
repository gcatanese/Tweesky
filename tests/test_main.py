import unittest

from src.main import generate_card, generate_card_as_html


class MainTest(unittest.TestCase):

    def test_generate_card(self):
        url = 'https://perosa.github.io/'
        card = generate_card(url)

        self.assertIsNotNone(card)
        self.assertEqual('Perosa', card.title)
        self.assertEqual(url, card.url)

    def test_generate_card_as_html(self):
        url = 'https://perosa.github.io/'
        html_card = generate_card_as_html(url)

        self.assertIsNotNone(html_card)

