import pytest
from cartomancy.games.core.deck import Deck


@pytest.fixture
def deck():
    return Deck()


def test_deck(deck):
    assert hasattr(deck, 'draw')
    assert hasattr(deck, 'shuffle')
    assert hasattr(deck, '__len__')
    assert hasattr(deck, '__str__')
