import pytest
from aicard.games.go_fish import GO_FISH_INITIAL_HAND_SIZE_MAP
from aicard.games.run import create_game
import configparser
import os


@pytest.fixture
def game():
    """Parse configs, create game, and play."""
    config_path = os.path.abspath('../../../aicard/games/config/')
    go_fish_ini_path = os.path.join(config_path,'go_fish/random.ini')

    # load config
    config = configparser.ConfigParser()
    config.read(go_fish_ini_path)

    # load game
    game = create_game(config)

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
