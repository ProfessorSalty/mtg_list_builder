from typing import List


class ColorDataResource:
    __combos: List[tuple]
    __base_color_names: List[str]
    __base_colors: List[str]

    @property
    def combos(self):
        return self.__combos

    @property
    def base_color_names(self):
        return self.__base_color_names

    @property
    def base_colors(self):
        return self.__base_colors

    def __init__(self, color_data):
        self.__combos = color_data['combos']
        self.__base_colors = color_data['base_colors']
        self.__base_color_names = color_data['base_color_name']
