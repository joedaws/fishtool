import numpy as np
from aicard.brains.spaces.go_fish.actions import Actions


class GoFishRandomPolicy:
    """Random policies for GoFish.

    The policy is instantiated by the game class during the game
    class's instantiation. The actions are provided at choice time and
    then passed to
    """
    def __init__(self):
        self._actions = None

    @property
    def actions(self):
        """An instance of the Actions class"""
        return self._actions

    @actions.setter
    def actions(self, new_actions: Actions):
        """Overwrite the actions stored in Actions."""
        self._actions = new_actions

    def rank_to_seek(self):
        """Choose a rank to ask an opponent for."""
        ranks = self.actions.valid_ranks
        ask_idx = np.random.randint(low=0, high=len(ranks))
        return ranks[ask_idx]

    def player_to_ask(self):
        """Choose a player from among the valid players"""
        opponents = self.actions.valid_opponents
        ask_idx = np.random.randint(low=0, high=len(opponents))
        return opponents[ask_idx]

    def sample(self):
        """Return the required choices."""
        return self.player_to_ask(), self.rank_to_seek()
