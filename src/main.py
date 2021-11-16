from src.output.html.html_output import get_html
from src.parser.parser_factory import get_parser


def generate_card(target_url):
    """
    Generate Social Media card
    :param target_url: url
    :return: Card object
    """

    parser = get_parser(target_url)
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