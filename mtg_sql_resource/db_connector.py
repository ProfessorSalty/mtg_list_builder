from typing import List

from pymysql import Connection, cursors

from .enums import CardRarity


class DB_Connector:
    class CardConnection:
        __db_connection: Connection

        def __init__(self, options):
            self.__db_connection = Connection(**options)

        def get_cards_in_set(self, card_set: str):
            statement = "SELECT name, artist, type as cardType, " \
                        "FormatColors(colorIdentity) as colorName, " \
                        "IsFoil(finishes) as isFoil, colors, isAlternative, rarity," \
                        "frameEffects " \
                        "FROM cards WHERE setCode = %s AND isPromo = FALSE " \
                        "ORDER BY colors, colorName, cardType, name, artist, frameEffects, isFoil;"
            return self.__execute_query(statement, card_set)

        def get_set(self, set_id: str):
            statement = "SELECT name, code, keyruneCode, baseSetSize, type, releaseDate " \
                        "FROM sets WHERE code = %s";
            return self.__execute_query(statement, set_id)[0]

        def get_set_cards_by_rarity(self, card_set: str, desired_rarities: List[CardRarity]):
            statement = "SELECT DISTINCT name " \
                        "FROM cards WHERE setCode = %s " \
                        "AND rarity in %s AND isPromo = FALSE " \
                        "AND isAlternative = FALSE AND (side IS NULL OR side = 'a');"
            return self.__execute_query(statement, card_set, desired_rarities)

        def close(self):
            self.__db_connection.close()

        def __execute_query(self, query_statement: str, *args):
            cursor = self.__db_connection.cursor()
            cursor.execute(query_statement, args)
            return cursor.fetchall()

    __db: CardConnection
    __options = {
        'host': '',
        'user': '',
        'password': '',
        'database': '',
        'cursorclass': '',
    }

    def __init__(self,
                 host='localhost',
                 user='user',
                 password='passwd',
                 database='db',
                 cursorclass=cursors.DictCursor):
        self.__options['host'] = host
        self.__options['user'] = user
        self.__options['password'] = password
        self.__options['database'] = database
        self.__options['cursorclass'] = cursorclass

    def __enter__(self):
        self.__db = self.CardConnection(self.__options)
        return self.__db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__db.close()
