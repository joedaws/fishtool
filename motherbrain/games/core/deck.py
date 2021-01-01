import random


class Deck:
    """Abstract class for deck.

    A Deck is a collection of cards stored as a list. The deck
    can be shuffled or drawn from.
    """
    def __init__(self):
        """Set the cards attribute to None."""
        self.cards = None

    def __str__(self):
        """printer friendly readout of cards.

        Note:
            All card classes geneerated by CardBuilder should have a
            str method.
        """
        s = ''
        for c in self.cards:
            s += str(c) + '\n'

        return s.rstrip()

    def __len__(self):
        """Number of cards currently in the deck."""
        return len(self.cards)

    def shuffle(self):
        """randomize the order of the deck"""
        random.shuffle(self.cards)

    def draw(self, n=1):
        """Draws n cards from the cards attribute.

        Note:
            This method removes n cards from the deck

        Returns:
            list: list of drawn card(s)
        """
        return [self.cards.pop() for _ in range(n)]
