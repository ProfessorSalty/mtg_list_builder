from mtg_sql_resource import MTGSQLResource, CardRarity


class BulkListGenerator:
    __db: MTGSQLResource

    def __init__(self, db: MTGSQLResource):
        self.__db = db

    def get_set_cards_by_rarity(self, set_name: str, desired_rarity: CardRarity):
        cards = self.__db.get_cards_by_rarity(set_name, desired_rarity)
        lines = [f"{card.name}" for card in cards]
        return "\n".join(lines)
