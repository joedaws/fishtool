

class Player:
    """A generic players class"""
    GAME = 'GENERIC'
    MAXIMUM_HAND_SIZE = 52

    def __init__(self, name):
        self.name = name
        self.card_type = None
        self.index = None
        self._hand = None
        self._deck = None

    @property
    def hand(self):
        """The players's hand, i.e., a list of card objects"""
        if self._hand is None:
            print(f'{self.GAME} {self.name} is initializing hand.')
            self._hand = []

        if len(self._hand) > self.MAXIMUM_HAND_SIZE:
            raise ValueError(f'Hand size exceeds maximum'\
                             f'handsize {self.MAXIMUM_HAND_SIZE}')

        return self._hand

    @hand.setter
    def hand(self, new_hand):
        """setter method for players's hand of cards"""
        self._hand = new_hand

    def draw(self, deck, n=1):
        """Player draws card(s) from provided deck.

        Args:
            deck (Deck): A instance of a card deck.
            n (int): Number of cards to draw from the deck.
        """
        new_cards = [deck.draw(1)[0] for _ in range(n)]
        self.receive(new_cards)

    def receive(self, new_card):
        """add card(s) to players's hand"""
        if self.card_type is None:
            self.card_type = type(new_card)

        if isinstance(new_card, list):
            self.hand += new_card

        elif isinstance(new_card, self.card_type):
            self.hand.append(new_card)

        else:
            raise ValueError(f"Cannot add {type(new_card)} to"
                             "{self.name}'s hand.")

    def remove(self, cards_to_remove):
        """Remove a card or cards from hand."""
        if not isinstance(cards_to_remove, list):
            cards_to_remove = [cards_to_remove]

        self.hand = [card for card in self.hand if str(card) not in
                     [str(c) for c in cards_to_remove]]

    def hand_str(self):
        """Returns single line string representation of hand"""
        hand_str = ""

        for c in self.hand:
            hand_str += str(c) + " "

        return hand_str

    def __str__(self):
        """Printable version of player"""
        return self.hand_str()

