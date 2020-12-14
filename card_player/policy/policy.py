import numpy as np
from copy import deepcopy


class random_policy:
    """Random policy for GoFishPlayer"""
    def __init__(self, hand):
        self.hand = deepcopy(hand)

    def rank_to_seek(self):
        """Choose a card whose rank you will to ask an opponent for."""
        ask_idx = np.random.randint(low=0, high=len(self.hand))
        return self.hand[ask_idx]

    def remove_card(self, card):
        """remove a card from hand"""
