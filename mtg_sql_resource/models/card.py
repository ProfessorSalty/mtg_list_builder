class Card:
    name: str
    artist: str
    card_type: str
    rarity: str
    color_name: str
    colors: str
    is_foil: bool
    is_alternative: bool
    frame_effects: str

    def __init__(self, card_data):
        self.name = card_data['name']
        self.artist = card_data['artist']
        self.card_type = card_data['cardType']
        self.color_name = card_data['colorName']
        if card_data['colors'] is not None:
            self.colors = card_data['colors'].split(',')
        else:
            self.colors = None
        self.is_foil = card_data['isFoil'] == 1
        self.is_alternative = card_data['isAlternative'] == 1

        if card_data['frameEffects'] is not None:
            self.frame_effects = card_data['frameEffects'].split(',')
        else:
            self.frame_effects = None
        self.rarity = card_data['rarity']


