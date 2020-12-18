from aicard.brains.spaces.go_fish.observations import Observations


class Actions:
    """Go Fish actions.

    In go fish a player must choose an opponent to ask and a rank to ask for.
    This action space determines who are the valid opponents to ask and
    what are the valid ranks to ask for.

    Note that the observed hand lengths are known exactly to the player at
    ask time.
    """

    def __init__(self, observations: Observations, hand: list):
        self.observed_hand_len = observations.observed_hand_len
        self.hand = hand

    @property
    def valid_opponents(self):
        """Returns list of opponents whom the players can ask a card from.

        You can only as an opponent for cards if they have cards to ask for.

        Returns:
            list of opponent indices of opponent players that have cards.
        """
        return [opponent for opponent in self.observed_hand_len.opponents
                if self.observed_hand_len[opponent].hand_len > 0]

    @property
    def valid_ranks(self):
        """Returns list of ranks which might possibly still be in play.

        A valid rank is any rank for which the player current has a card.

        Returns:
            a list ranks in the players hand.
        """
        return [card.rank for card in self.hand]

    def get_possible_actions(self):
        return self.valid_opponents, self.valid_ranks
