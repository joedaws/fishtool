import random
from card_player.deck import ALLOWED_SUITS, ALLOWED_RANKS
from card_player.deck import Card, Joker

class Deck():
    """standard 52 or 54 card deck
    TODO should consider making some of the these mehtods into 
    an abstract base class. Then a deck inherits from a abstract 
    card collection.
    """
    def __init__(self, joker=False, shuffle_start=False):
        """
        Args:
            joker (bool): if True then deck contains 2 joker cards
                if False then the deck doesn't contain joker cards.
            shuffle_start (bool): if True then the deck is shuffled
                on initialization.
        """
        # set joker type
        self.joker = joker

        # set deck
        if joker:
            self.cards = _setup_standard_54()

        else:
            self.cards = _setup_standard_52()

        # shuffle
        if shuffle_start:
            self.shuffle()

    def __str__(self):
        """printer friendly readout of cards"""
        s = ''
        for c in self.cards:
            s += str(c) + '\n'

        return s.rstrip()

    def shuffle(self):
        """randomize the order of the deck"""
        _shuffle(self.cards)

    def draw(self, n=1):
        """draws n cards from the cards attribute

        Note:
            This method removes n cards from the deck

        Returns:
            list: list of drawn card(s)
        """
        return [self.cards.pop() for _ in range(n)]

def _setup_standard_52():
    """build a standard 52 card deck."""
    return [Card(suit, rank) for suit in ALLOWED_SUITS for rank in ALLOWED_RANKS]

def _setup_standard_54():
    return _setup_standard_52() + [Joker(), Joker()]

def _shuffle(deck):
    """shuffles a deck"""
    random.shuffle(deck)
