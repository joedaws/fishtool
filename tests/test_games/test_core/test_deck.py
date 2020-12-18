import pytest
from aicard.games.core.deck import Deck
from aicard.players.go_fish import GoFishPlayer

HAND_SIZE = 7

@pytest.fixture
def players():
    p1 = GoFishPlayer('player1')
    p2 = GoFishPlayer('player2')
    return [p1, p2]

@pytest.fixture
def deck():
    return Deck()


def test_deal_and_shuffle(players, deck):
    # make a deck
    deck.shuffle()

    # deal some cards
    for _ in range(HAND_SIZE):
        for p in players:
            p.draw(deck)
    
    for p in players:
        assert len(p.hand) == HAND_SIZE


def test_ask(players, deck):
    # deal some cards
    for _ in range(HAND_SIZE):
        for p in players:
            p.draw(deck)

    # player1 asks for a card from player2
    ask_rank = players[0].hand[0].rank
    players[0].ask(players[1],ask_rank)
    assert 1
