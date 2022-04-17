import requests
import logging
from bs4 import BeautifulSoup

from tweesky.model.card import Card
import json


class HtmlParser:
    "Parser of HTML pages"

    def __init__(self, url=None, html=None):
        """
        HtmlParser constructor
        :param url: URL of the web page
        :param html: HTML content
        """
        self.url = url
        self.html = html
        self.r = None
        self.soup = None
        self.titleNotFound = False
        self.descriptionNotFound = False

        if self.url is not None:
            # HTTP fetch (when URL is defined)
            self.r = requests.get(self.url, headers=self.get_headers())
            self.html = self.r.text

        self.soup = BeautifulSoup(self.html, "lxml")

    def get_card(self):

        # logging.info(self.html)

        card = Card()
        card.url = self.url
        card.twitter_card = self.find_twitter_card()
        card.title = self.find_title()
        card.description = self.find_description()
        card.image = self.find_image()
        card.twitter_site = self.find_twitter_site()
        card.twitter_site_id = self.find_twitter_site_id()
        card.twitter_creator = self.find_twitter_creator()
        card.twitter_creator_id = self.find_twitter_creator_id()
        card.twitter_image_alt = self.find_twitter_image_alt()
        # Twitter player
        card.twitter_player = self.find_twitter_player()
        card.twitter_player_stream = self.find_twitter_player_stream()
        card.twitter_player_width = self.find_twitter_player_width()
        card.twitter_player_height = self.find_twitter_player_height()

        card.twitter_app_country = self.find_twitter_app_country()

        # Twitter iphone app
        card.twitter_app_id_iphone = self.find_twitter_app_id_iphone()
        card.twitter_app_name_iphone = self.find_twitter_app_name_iphone()
        card.twitter_app_url_iphone = self.find_twitter_app_url_iphone()
        # Twitter ipad app
        card.twitter_app_id_ipad = self.find_twitter_app_id_ipad()
        card.twitter_app_name_ipad = self.find_twitter_app_name_ipad()
        card.twitter_app_url_ipad = self.find_twitter_app_url_ipad()
        # Twitter googleplay app
        card.twitter_app_id_googleplay = self.find_twitter_app_id_googleplay()
        card.twitter_app_name_googleplay = self.find_twitter_app_name_googleplay()
        card.twitter_app_url_googleplay = self.find_twitter_app_url_googleplay()

        return card

    def find_twitter_card(self):

        twitter_card = self.find_twitter_meta('twitter:card')

        if twitter_card is None:
            # default value
            twitter_card = 'summary_large_image'

        return twitter_card

    def find_title(self):

        twitter_title = self.soup.find(attrs={'name': 'twitter:title'})

        if twitter_title is not None:
            return twitter_title.get('content')

        twitter_title = self.find_og_title()
        if twitter_title is not None:
            return twitter_title.get('content')

        twitter_title = self.find_schema_name()
        if twitter_title is not None:
            return twitter_title

        twitter_title = self.soup.find('title')
        if twitter_title is not None:
            return twitter_title.string

        self.titleNotFound = True
        return 'n/a'

    def has_title(self):
        title = self.find_title()

        if title == 'n/a':
            return False
        else:
            return True

    def find_og_title(self):
        og_title = self.soup.find("meta", attrs={'property': 'og:title'})

        return og_title

    def find_tag_title(self):
        title = self.soup.find('title')

        return title

    def find_description(self):

        twitter_description = self.soup.find(attrs={'name': 'twitter:description'})
        if twitter_description is not None:
            return twitter_description.get('content')

        twitter_description = self.find_og_description()
        if twitter_description is not None:
            return twitter_description.get('content')

        twitter_description = self.find_schema_description()
        if twitter_description is not None:
            return twitter_description

        twitter_description = self.find_meta_tag_description()
        if twitter_description is not None:
            return twitter_description.get('content')

        twitter_description = self.find_tag_description()
        if twitter_description is not None:
            return twitter_description.string

        self.descriptionNotFound = True
        return ''

    def find_og_description(self):
        og_description = self.soup.find("meta", attrs={'property': 'og:description'})

        return og_description

    def find_meta_tag_description(self):
        description = self.soup.find("meta", attrs={'name': 'description'})

        return description

    def find_tag_description(self):
        description = self.soup.find('description')

        return description

    def find_image(self):

        twitter_image = self.soup.find(attrs={'name': 'twitter:image'})
        if twitter_image is not None:
            content = twitter_image.get('content')
            if self.is_valid_url(content):
                return content

        twitter_image = self.find_og_image()
        if twitter_image is not None:
            content = twitter_image.get('content')
            if self.is_valid_url(content):
                return content

        logo = self.find_schema_image()
        if logo is not None and self.is_valid_url(logo):
            return logo

        return 'n/a'

    def find_og_image(self):
        og_image = self.soup.find("meta", attrs={'property': 'og:image'})

        return og_image

    def find_schema_image(self):
        logo = None

        schema_org_script = self.find_schema_org_script()

        if schema_org_script is not None:
            if 'logo' in schema_org_script:
                logo = self.find_schema_image_element(schema_org_script['logo'])
            elif 'image' in schema_org_script:
                logo = self.find_schema_image_element(schema_org_script['image'])

        logging.debug(f'schema_org logo {logo}')

        return logo

    def find_schema_image_element(self, image):
        if '@type' in image and image['@type'] == 'ImageObject':
            if 'url' in image:
                return self.get_single_value(image['url'])

        if isinstance(image, str):
            return image

        if isinstance(image, list):
            return image[0]

        return None

    def get_single_value(self, value):
        if isinstance(value, list):
            return value[0]
        else:
            return value

    def find_schema_name(self):
        name = None

        schema_org_script = self.find_schema_org_script()

        if schema_org_script is not None:
            if 'name' in schema_org_script:
                name = schema_org_script['name']

        return name

    def find_schema_description(self):
        name = None

        schema_org_script = self.find_schema_org_script()

        if schema_org_script is not None:
            if 'description' in schema_org_script:
                name = schema_org_script['description']

        return name

    def find_schema_org_script(self):
        schema_org_script = None

        schema_org = self.soup.find('script', type='application/ld+json')

        if schema_org is not None:
            schema_org_script = json.loads(schema_org.string)

            if schema_org_script is not None:
                # found array
                if '@graph' in schema_org_script:
                    schema_org_script = schema_org_script['@graph'][0]

            if '@type' not in schema_org_script:
                # type not found: discard schema org info
                logging.warning('Ignore Schema Org json: @type attribute is undefined')
                schema_org_script = None

        return schema_org_script

    def find_twitter_site(self):
        return self.find_twitter_meta('twitter:site')

    def find_twitter_site_id(self):
        return self.find_twitter_meta('twitter:site:id')

    def find_twitter_creator(self):
        return self.find_twitter_meta('twitter:creator')

    def find_twitter_creator_id(self):
        return self.find_twitter_meta('twitter:creator:id')

    def find_twitter_player(self):
        return self.find_twitter_meta('twitter:player')

    def find_twitter_player_stream(self):
        return self.find_twitter_meta('twitter:player:stream')

    def find_twitter_player_width(self):
        return self.find_twitter_meta('twitter:player:width')

    def find_twitter_player_height(self):
        return self.find_twitter_meta('twitter:player:height')

    def find_twitter_image_alt(self):
        return self.find_twitter_meta('twitter:image:alt')

    def find_twitter_app_id_iphone(self):
        return self.find_twitter_meta('twitter:app:id:iphone')

    def find_twitter_app_name_iphone(self):
        return self.find_twitter_meta('twitter:app:name:iphone')

    def find_twitter_app_url_iphone(self):
        return self.find_twitter_meta('twitter:app:url:iphone')

    def find_twitter_app_id_ipad(self):
        return self.find_twitter_meta('twitter:app:id:ipad')

    def find_twitter_app_name_ipad(self):
        return self.find_twitter_meta('twitter:app:name:ipad')

    def find_twitter_app_url_ipad(self):
        return self.find_twitter_meta('twitter:app:url:ipad')

    def find_twitter_app_id_googleplay(self):
        return self.find_twitter_meta('twitter:app:id:googleplay')

    def find_twitter_app_name_googleplay(self):
        return self.find_twitter_meta('twitter:app:name:googleplay')

    def find_twitter_app_url_googleplay(self):
        return self.find_twitter_meta('twitter:app:url:googleplay')

    def find_twitter_app_country(self):
        return self.find_twitter_meta('twitter:app:country')

    def find_twitter_meta(self, meta_name):
        res = None

        twitter_meta = self.soup.find(attrs={'name': meta_name})

        if twitter_meta is None:
            twitter_meta = self.soup.find(attrs={'property': meta_name})

        if twitter_meta is not None:
            res = twitter_meta.get('content')

        return res

    def is_valid_url(self, url):
        return url.lower().startswith('http')

    # HTTP Headers
    def get_headers(self):
        return {'User-Agent': self.get_browser_user_agent(),
                'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, image/apng,'
                          ' */*;q=0.8, application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-GB,en;q=0.9'}

    # User-Agent HTTP Header
    def get_browser_user_agent(self):
        return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) ' \
               'Chrome/83.0.4103.61 Safari/537.36 '
