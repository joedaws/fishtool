from abc import ABC, abstractmethod
from card_player.deck import ALLOWED_RANKS, ALLOWED_SUITS


class AbstractCard(ABC):
    """Might be used in the future"""
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass


class Card:
    """standard playing card from a 52 or 54 card deck"""
    def __init__(self,suit,rank):
        if suit in ALLOWED_SUITS:
            self._suit = suit
        else:
            raise ValueError(f'{suit} is not a valid suit.')
        
        if rank in ALLOWED_RANKS:
            self._rank = rank
        else:
            raise ValueError(f'{rank} is not a valid rank.')

    def __str__(self):
        s = f'{self.rank} of {self.suit}'
        return s

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

class Joker:
    """Joker card"""
    suit = 'Joker'
    rank = 'Joker'

    def __str__(self):
        return 'Joker'
