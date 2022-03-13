from tweesky.output.json.json_output import get_json
from tweesky.output.html.html_output import get_html
from tweesky.parser.parser_factory import get_parser


def generate_card(url=None, html=None):
    """
    Generate Social Media card from a given URL or HTML document
    :param url: url of the web page
    :param html: HTML document
    :return: Card object
    """

    if url is None and html is None:
        raise Exception("Provide either a URL or an HTML document")

    parser = get_parser(url, html)
    card = parser.get_card()

    return card


def generate_card_as_html(url=None, html=None):
    """
    Generate Social Media card
    :param url: url
    :param html: HTML document
    :return: HTML page with OpenGraph and Twitter metadata
    """

    card = generate_card(url, html)
    html_card = get_html(card)

    return html_card


def generate_card_as_json(url=None, html=None):
    """
    Generate Social Media card
    :param target_url: url
    :param html: HTML document
    :return: Card object as JSON
    """

    card = generate_card(url, html)
    json_card = get_json(card)

    return json_card
