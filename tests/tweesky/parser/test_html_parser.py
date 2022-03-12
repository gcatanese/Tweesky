import unittest

from tweesky.parser.html_parser import HtmlParser


class HtmlParserTest(unittest.TestCase):

    def test_fetch(self):
        url = 'https://perosa.github.io/'

        parser = HtmlParser(url)

        card = parser.get_card()

        self.assertIsNotNone(parser.soup)
        self.assertIsNotNone(card)

    def test_find_basic_html(self):
        with open('tests/tweesky/resources/html/basic.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        self.assertEqual("summary", parser.find_twitter_card())
        self.assertEqual("My Site", parser.find_title())
        self.assertEqual("My Site Homepage", parser.find_description())

    def test_find_twitter_card(self):
        with open('tests/tweesky/resources/html/default.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        self.assertEqual("summary", parser.find_twitter_card())

    def test_find_title(self):
        with open('tests/tweesky/resources/html/default.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        self.assertEqual("Perosa", parser.find_title())

    def test_find_title_from_schema_org(self):
        with open('tests/tweesky/resources/html/html-with-schema-org.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        self.assertEqual("TOUR360 XT-SL Spikeless", parser.find_title())

    def test_find_tag_title(self):
        with open('tests/tweesky/resources/html/default.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        title = parser.find_tag_title()

        self.assertEqual("My Site", title.string)

    def test_find_description(self):
        with open('tests/tweesky/resources/html/default.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        description = parser.find_description()

        self.assertTrue("#chatbots #webhoooks #abtesting" in description)

    def test_find_description_from_schema_org(self):
        with open('tests/tweesky/resources/html/html-with-schema-org.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        description = parser.find_description()

        self.assertTrue("Comfort and confidence go " in description)

    def test_find_image(self):
        with open('tests/tweesky/resources/html/default.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        image = parser.find_image()

        self.assertEqual("https://perosa.github.io/images/perosa.png", image)

    def test_find_image_from_schema_org(self):
        with open('tests/tweesky/resources/html/html-with-schema-org.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        image = parser.find_image()

        self.assertEqual(
            "https://assets.adidas.com/images/w_600,f_auto,q_auto/501fbd6ed691421db4f2abd100ebb2a1_9366/"
            "TOUR360_XT_SL_Spikeless_Textile_Golf_Shoes_White_EG4875_01_standard.jpg",
            image)

    def test_find_image_from_schema_org_array(self):
        with open('tests/tweesky/resources/html/html-with-schema-org-array.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        image = parser.find_image()

        self.assertEqual("https://perosa.github.io/static/perosa.jpg", image)

    def test_schema_org_script_not_found(self):
        with open('tests/tweesky/resources/html/default.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        ld_script = parser.find_schema_org_script()

        self.assertIsNone(ld_script)

    def test_find_schema_org_script(self):
        with open('tests/tweesky/resources/html/html-with-schema-org.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        ld_script = parser.find_schema_org_script()
        # print(ld_script)

        self.assertIsNotNone(ld_script)

    def test_find_schema_org_script_with_array(self):
        with open('tests/tweesky/resources/html/html-with-schema-org-array.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        ld_script = parser.find_schema_org_script()
        # print(ld_script)

        self.assertIsNotNone(ld_script)

    def test_find_site_with_twitter_meta(self):
        with open('tests/tweesky/resources/html/html-with-twitter-cards-tags.html', 'r') as file:
            data = file.read().replace('\n', '')

        parser = HtmlParser(html=data)

        card = parser.get_card()

        self.assertEqual("player", card.twitter_card)
        self.assertEqual("Deep Space", card.title)
        self.assertEqual("Deep Space explained", card.description)

        self.assertEqual("@perosa", card.twitter_site)
        self.assertEqual("https://widget.perosa.com/player?episode_id=1.jpg", card.twitter_player)
        self.assertEqual("500", card.twitter_player_width)
        self.assertEqual("400", card.twitter_player_height)

        self.assertEqual("388449677", card.twitter_app_id_iphone)
        self.assertEqual("NL", card.twitter_app_country)
