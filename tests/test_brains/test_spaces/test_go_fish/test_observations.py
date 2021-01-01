import pytest
from motherbrain.players.go_fish import GoFishPlayer
from motherbrain.brains.spaces.go_fish.observations import Observations
from motherbrain.games.core.events import BookEvent, AskEvent, DrawEvent
from motherbrain.games.core.deck import Deck


@pytest.fixture
def players():
    p1 = GoFishPlayer('p1')
    p2 = GoFishPlayer('p2')
    p3 = GoFishPlayer('p3')
    p4 = GoFishPlayer('p4')
    return [p1, p2, p3, p4]


@pytest.fixture
def observation(players):
    player = players[0]
    opponents = [players[1], players[2], players[3]]
    obs = Observations(player=player, opponents=opponents)
    return obs


def test_obs(players, observation):
    """test that hand length increases after a draw"""
    assert hasattr(observation, 'player')
    assert observation.player == players[0]
    assert hasattr(observation, 'opponents')
    for opp in observation.opponents:
        assert opp in observation.opponents
    assert hasattr(observation, 'num_opponents')
    assert observation.num_opponents == 3
    assert hasattr(observation, 'observed_ranks')
    assert hasattr(observation, 'observed_hand_len')
