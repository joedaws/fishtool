# ALlowed suits
ALLOWED_SUITS = ['Hearts','Diamonds','Clubs','Spades']
# Allowed ranks
ALLOWED_RANKS = ['Ace'] + [str(i) for i in range(2,11)] + ['Jack','Queen','King']

from aicard.deck.card import Card, Joker
from aicard.deck.deck import Deck
