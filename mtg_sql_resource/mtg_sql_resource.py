import datetime

from mtg_sql_resource.db_connector import DB_Connector


class Card:
    name: str
    artist: str
    card_type: str
    rarity: str
    color_name: str
    colors: [str]
    is_foil: bool
    is_alternative: bool
    frame_effects: [str]

    def __init__(self, card_data):
        self.name = card_data['name']
        self.artist = card_data['artist']
        self.card_type = card_data['cardType']
        self.color_name = card_data['colorName']
        self.colors = card_data['colors']
        self.is_foil = card_data['isFoil'] == 1
        self.is_alternative = card_data['isAlternative'] == 1
        self.frame_effects = card_data['frameEffects']
        self.rarity = card_data['rarity']


class Set:
    name: str
    keyrune_code: str
    code: str
    base_set_size: int
    type: str
    release_date: datetime.date
    cards: [Card]
    rarity_totals: []
    color_totals: [(str, int)]
    multi_color_totals: [(str, int)]

    def __init__(self, set_data):
        self.name = set_data['name']
        self.keyrune_code = set_data['keyruneCode']
        self.code = set_data['code']
        self.base_set_size = set_data['baseSetSize']
        self.type = set_data['type']
        self.release_date = set_data['releaseDate']


class MTGSQLResource:
    db: DB_Connector
    default_db_options = {
        'database': 'db',
    }

    @staticmethod
    def instantiate(db_user: str, db_pass: str, **kwargs):
        if db_user is None or db_pass is None:
            raise Exception('both db_user and db_pass are required')

        options = {
            'user': db_user,
            'password': db_pass,
            **MTGSQLResource.default_db_options,
            **kwargs,
        }
        _db = DB_Connector(**options)
        list_app = MTGSQLResource(_db)

        return list_app

    def __init__(self, _db):
        self.db = _db

    def get_cards_in_set(self, card_set: str):
        with self.db as card_db:
            cards = card_db.get_cards_in_set(card_set)
            return [Card(card) for card in cards]

    def get_set(self, set_id: str):
        with self.db as card_db:
            set_data = card_db.get_set(set_id)
            new_set = Set(set_data)
            set_cards = [Card(card) for card in card_db.get_cards_in_set(new_set.code)]
            new_set.cards = set_cards
            return new_set
