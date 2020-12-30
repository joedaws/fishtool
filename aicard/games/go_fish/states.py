from aicard.players.go_fish import GoFishPlayer
from aicard.games.core.deck import Deck
from aicard.brains.spaces.go_fish.observations import Observations


class GoFishState:
    """A class representing the state of the go fish game."""

    def __init__(self, num_players=4):
        player_names = ['player ' + str(i) for i in range(num_players)]
        self.players = {GoFishPlayer(name): i for i, name in enumerate(player_names)}
        self._set_player_indices()
        self.opponents_map = self._setup_opponents_map()

        self.deck = Deck()

        self.observations = {player: Observations(player, self.opponents_map[player])
                             for player in self.players}

    def reset(self):
        """Reset to an initial state."""
        self.deck = Deck()
        self.observations = {player: Observations(player, self.opponents_map[player])
                             for player in self.players}

    def hands(self):
        """Returns hands of all players.

        Returns:
            dictionary whose keys are players and whose values are the corresponding player's hand.
        """
        return {player: player.hand for player in self.players}

    def update(self, event):
        """update the state according to the event."""

        # update observations
        for player in self.players:
            self.observations[player].update(event)

    def _set_player_indices(self):
        """Set the index attribute of the players."""
        for player, index in self.players.items():
            player.index = index

    def _setup_opponents_map(self):
        """Create a dictionary describing the opponents of each players."""
        indices = list(self.players.values())
        return {player: [opponent for opponent in self.players if opponent != player] for player in self.players}
