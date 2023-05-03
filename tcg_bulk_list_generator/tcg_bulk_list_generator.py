from mtg_sql_resource import MTGSQLResource, CardRarity

class TcgBulkListGenerator:
    __db: MTGSQLResource

    def __init__(self, db: MTGSQLResource):
        self.__db = db

    def get_set_cards_by_rarity(self, set_name: str, desired_rarity: CardRarity):
        pass