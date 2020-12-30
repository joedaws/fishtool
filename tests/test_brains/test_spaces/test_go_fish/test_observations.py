import pytest
from aicard.players.go_fish import GoFishPlayer
from aicard.brains.spaces.go_fish.observations import Observations
from aicard.games.core.events import BookEvent, AskEvent, DrawEvent
from aicard.games.core.deck import Deck


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


def test_update_draw_event(players, observation):
    """test that hand length increases after a draw"""
    for opponent in observation.opponents:
        opponent.draw(deck=Deck(), n=1)
        draw = DrawEvent(player=opponent, number=1)
        observation.update(draw)
        ranks, number = observation.get_observation(opponent)
        assert number == 1
