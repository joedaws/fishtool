import numpy as np
from aicard.brains.spaces.go_fish.actions import Actions


class GoFishRandomPolicy:
    """Random policies for GoFish"""
    def __init__(self, actions: Actions):
        self.actions = actions

    def rank_to_seek(self):
        """Choose a rank to ask an opponent for."""
        ranks = self.actions.valid_ranks
        ask_idx = np.random.randint(low=0, high=len(ranks))
        return ranks[ask_idx]

    def player_to_ask(self):
        opponents = self.actions.valid_opponents
        ask_idx = np.random.randint(low=0, high=len(opponents))
        return opponents[ask_idx]

    def sample(self):
        return self.player_to_ask(), self.rank_to_seek()
