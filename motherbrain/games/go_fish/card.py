NAME = "Standard"
CARD_FIELDS = [('rank', str), ('suit', str)]
CARD_STR_FUN = lambda self: f"{self.rank} of {self.suit}"
CARD_FIELD_VALUES = {'suit': ['Hearts', 'Diamonds', 'Clubs', 'Spades'],
                     'rank': ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King']}


def card_generator():
    return ({'suit': suit, 'rank': rank}
            for suit in CARD_FIELD_VALUES['suit']
            for rank in CARD_FIELD_VALUES['rank'])
