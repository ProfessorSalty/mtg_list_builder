from mtg_sql_resource import Set, Card
from mtg_sql_resource.db_connector import DB_Connector


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

    def get_set(self, set_id: str):
        with self.db as card_db:
            set_data = card_db.get_set(set_id)
            new_set = Set(set_data)
            set_cards = [{**vars(Card(card))} for card in card_db.get_cards_in_set(new_set.code)]
            new_set.cards = set_cards
            return new_set
