class SetIconImageConfiguration:
    __text_color: str
    __title_stroke_color: str
    __icon_color: str

    def __init__(self, config: dict):
        self.__text_color = config["text_color"]
        self.__title_stroke_color = config["title_stroke_color"]
        self.__icon_color = config["icon_color"]

    @property
    def text_color(self) -> str:
        return self.__text_color

    @property
    def title_stroke_color(self) -> str:
        return self.__title_stroke_color

    @property
    def icon_color(self) -> str:
        return self.__icon_color

