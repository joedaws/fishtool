import pytest
from cartomancy.games.go_fish import INITIAL_HAND_SIZE_MAP
from cartomancy.games.run import create_game
from cartomancy import CARTOMANCY_PATH
import yaml
from yaml import Loader
import os


@pytest.fixture
def game():
    """Parse configs, create game, and play."""
    go_fish_config_path = 'config/go_fish/random.yaml'

    # load config
    with open(go_fish_config_path, 'rb') as stream:
        config = yaml.load(stream, Loader=Loader)

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
        assert len(player.hand) == INITIAL_HAND_SIZE_MAP[game.num_players]

    # check observations
    for player, obs in game.state.observations.items():
        for opponent in obs.opponents:
            assert obs.observed_hand_len[opponent].hand_len == INITIAL_HAND_SIZE_MAP[game.num_players]
            assert obs.observed_ranks[opponent].ranks['2'] == 0

    # check that deck has correct amount of cards
    assert len(game.state.deck.cards) == 52 - 4*5


def test_turn(game):
    game.reset()
    game.deal()
    game.turn()
