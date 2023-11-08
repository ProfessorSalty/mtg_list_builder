from typing import List


class SetRarity:
    __set_name: str
    __rarities: List[str]

    @property
    def set_name(self):
        return self.__set_name

    @property
    def rarities(self):
        return self.__rarities

    @staticmethod
    def __process_input_arg(input_args: str):
        res = input_args.split(':')
        rarities = [rarity.strip() for rarity in res[1].split(',')]
        if len(res) != 2:
            raise Exception(f"Malformed argument {input_args}")
        return res[0], rarities

    @staticmethod
    def create_list_from_input_args(input_args: List[str]):
        processed_args = [SetRarity.__process_input_arg(arg) for arg in input_args[1:]]
        return [SetRarity(set_name, rarities) for set_name, rarities in processed_args]

    def __init__(self, set_name: str, rarities: List[str]):
        self.__set_name = set_name
        self.__rarities = rarities
