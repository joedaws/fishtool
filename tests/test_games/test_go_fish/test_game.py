import pytest
from aicard.games.go_fish.game import GoFishGame
from aicard.games.go_fish import GO_FISH_INITIAL_HAND_SIZE_MAP


@pytest.fixture
def game():
    num_players = 4
    game = GoFishGame(num_players)
    return game


def test_attributes(game):
    assert game.state
    assert game.num_players
    assert game.turn


def test_deal(game):
    game.reset()
    game.deal()

    # check player hands
    for player in game.state.players:
        assert len(player.hand) == GO_FISH_INITIAL_HAND_SIZE_MAP[game.num_players]

    # check observations
    for player, obs in game.state.observations.items():
        for opponent in obs.opponents:
            assert obs.observed_hand_len[opponent].hand_len == GO_FISH_INITIAL_HAND_SIZE_MAP[game.num_players]
            assert obs.observed_ranks[opponent].ranks['2'] == 0

    # check that deck has correct amount of cards
    assert len(game.state.deck.cards) == 52 - 4*5


def test_turn(game):
    game.reset()
    game.deal()
    game.turn()
