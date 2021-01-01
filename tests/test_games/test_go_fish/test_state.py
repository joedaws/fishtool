from aicard.games.go_fish.state import GoFishState
from aicard.players.go_fish import GoFishPlayer


def test_state():
    num_players = 4
    state = GoFishState(num_players=num_players)
    assert len(state.players) == num_players
    assert len(state.observations) == num_players

    for player in state.players:
        assert isinstance(player, GoFishPlayer)
