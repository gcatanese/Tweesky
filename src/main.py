from output.json.json_output import get_json
from src.output.html.html_output import get_html
from src.parser.parser_factory import get_parser


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
    parser.fetch()
    card = parser.get_card()

    return card


def generate_card_as_html(target_url):
    """
    Generate Social Media card
    :param target_url: url
    :return: HTML page with OpenGraph and Twitter metadata
    """

    card = generate_card(target_url)
    html_card = get_html(card)

    return html_card


def generate_card_as_json(target_url):
    """
    Generate Social Media card
    :param target_url: url
    :return: JSON document with OpenGraph and Twitter metadata
    """

    card = generate_card(target_url)
    json_card = get_json(card)

    return json_card
