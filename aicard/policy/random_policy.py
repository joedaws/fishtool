import numpy as np


class GoFishRandomPolicy:
    """Random policy for GoFish"""
    def __init__(self, observation, valid_actions):
        self.observation = observation

    def rank_to_seek(self):
        """Choose a card whose rank you will to ask an opponent for."""
        ask_idx = np.random.randint(low=0, high=len(self.hand))
        return self.hand[ask_idx].rank

    def player_to_ask(self):
        return 0
