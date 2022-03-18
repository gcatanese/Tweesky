import json


def get_json(card):
    return json.dumps(card.__dict__)
