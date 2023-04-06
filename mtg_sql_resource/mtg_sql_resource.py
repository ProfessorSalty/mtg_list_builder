import datetime

from mtg_sql_resource.db_connector import DB_Connector


class Set:
    name: str
    keyrune_code: str
    code: str
    base_set_size: int
    type: str
    release_date: datetime.date

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
            return card_db.get_cards_in_set(card_set)

    def get_set(self, set_id: str):
        with self.db as card_db:
            set_data = card_db.get_set(set_id)
            return Set(set_data)
