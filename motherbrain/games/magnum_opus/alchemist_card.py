"""
At a minimum this file should contain:
    NAME: Camel case name of game

For a card game which uses card builders and deck builders,
this file should contain:
    CARD_FIELDS: List of tuples e.g. [(<field_name>, <field_type>)]
    CARD_STR_FUN: callable which returns string for card instances, e.g.,
                  lambda self: f"{self.name}"
    CARD_FIELD_VALUES: dictionary whose keys are field names from CARD_FIELDS and whose values
                       are lists of allowed values for these fields, e.g.,
                       {'suit': ['Hearts', 'Diamonds', 'Clubs', 'Spades'],
                        'rank': ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King']}
    card_generator: A callable which returns a generator of tupes representing the cards in the deck.

                    def card_generator():
                        return ({'suit': suit, 'rank': rank}
                        for suit in CARD_FIELD_VALUES['suit']
                        for rank in CARD_FIELD_VALUES['rank'])
""""""
At a minimum this file should contain:
    NAME: Camel case name of game

For a card game which uses card builders and deck builders,
this file should contain:
    CARD_FIELDS: List of tuples e.g. [(<field_name>, <field_type>)]
    CARD_STR_FUN: callable which returns string for card instances, e.g.,
                  lambda self: f"{self.name}"
    CARD_FIELD_VALUES: dictionary whose keys are field names from CARD_FIELDS and whose values
                       are lists of allowed values for these fields, e.g.,
                       {'suit': ['Hearts', 'Diamonds', 'Clubs', 'Spades'],
                        'rank': ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King']}
    card_generator: A callable which returns a generator of tupes representing the cards in the deck.

                    def card_generator():
                        return ({'suit': suit, 'rank': rank}
                        for suit in CARD_FIELD_VALUES['suit']
                        for rank in CARD_FIELD_VALUES['rank'])
"""
from faker import Faker
fake = Faker()


NAME = "MagnumOpus"
NUM_ALCHEMISTS = 10
CARD_FIELDS = [('name', str), ('sign', str), ('element', str)]
CARD_STR_FUN = lambda self: f"{self.name} the {self.sign}"
CARD_FIELD_VALUES = {'name': [fake.name() for _ in range(NUM_ALCHEMISTS)],
                               'sign': ['Aries', 'Taurus', 'Gemini',
                                        'Cancer', 'Leo', 'Virgo',
                                        'Libra', 'Scorpio', 'Sagittarius',
                                        'Capricorn', 'Aquarius', 'Pisces'],
                               'element': ['Fire', 'Earth', 'Air', 'Water']}

ELEMENT_MAP = {'Aries': 'Fire', 'Taurus': 'Earth', 'Gemini': 'Air',
               'Cancer': 'Water', 'Leo': 'Fire', 'Virgo': 'Earth',
               'Libra': 'Air', 'Scorpio': 'Water', 'Sagittarius': 'Fire',
               'Capricorn': 'Earth', 'Aquarius': 'Air', 'Pisces': 'Water'}


def card_generator():
    return ({'name': fake.name(), 'sign': sign, 'element': ELEMENT_MAP[sign]}
            for sign in CARD_FIELD_VALUES['sign']
            for _ in range(2))
