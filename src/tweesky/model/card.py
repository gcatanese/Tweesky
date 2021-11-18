class Card:
    "Card object"

    # original URL
    url = ''

    title = ''
    description = ''
    image = ''
    twitter_card = ''
    twitter_image_alt = ''
    twitter_site = ''
    twitter_site_id = ''
    twitter_creator = ''
    twitter_creator_id = ''
    # Twitter player
    twitter_player = ''
    twitter_player_width = ''
    twitter_player_height = ''
    twitter_player_stream = ''
    # Twitter iphone app
    twitter_app_id_iphone = ''
    twitter_app_url_iphone = ''
    twitter_app_name_iphone = ''
    # Twitter ipad app
    twitter_app_id_ipad = ''
    twitter_app_url_ipad = ''
    twitter_app_name_ipad = ''
    # Twitter googleplay app
    twitter_app_id_googleplay = ''
    twitter_app_url_googleplay = ''
    twitter_app_name_googleplay = ''

    twitter_app_country = ''

    def __str__(self):
        return f'Card[url={self.url}, title={self.title}]'
