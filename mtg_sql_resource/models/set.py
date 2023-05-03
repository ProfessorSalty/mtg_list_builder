from datetime import datetime
from typing import List

from mtg_sql_resource.models.card import Card


class Set:
    name: str
    keyrune_code: str
    code: str
    base_set_size: int
    type: str
    release_date: datetime.date
    cards: List[Card]

    def __init__(self, set_data):
        self.name = set_data['name']
        self.keyrune_code = set_data['keyruneCode']
        self.code = set_data['code']
        self.base_set_size = set_data['baseSetSize']
        self.type = set_data['type']
        self.release_date = set_data['releaseDate']


