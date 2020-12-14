from card_player.deck import Deck
from card_player.deck import Card
from card_player.deck import ALLOWED_RANKS
from card_player.player import Player


class GoFishPlayer(Player):
    """A go Fish player class."""
    GAME = 'GoFish'
    def __init__(self, name):
        super().__init__(name)
        self.books = []

    @property
    def state(self):
        """A dictionary for describing contents of hand.

        The keys are the allowed ranks that the player current
        has in their hand and the values are lists
        of suits of the cards of that rank.
        """
        if self.hand is None:
            raise ValueError(f'Cannot compute state for uninitialized hand.')

        state = {rank:[] for rank in ALLOWED_RANKS}

        for card in self.hand:
            state[card.rank].append(card.suit)

        return state

    def look_for_rank_match(self, rank):
        """Find all cards in hand  matching a given rank"""
        if rank not in ALLOWED_RANKS:
            raise ValueError(f'{rank} is not a valid rank.')

        rank_matched_cards = [card for card in self.hand if card.rank == rank]

        return rank_matched_cards

    def check_for_books(self):
        """check hand for books

        If a book is found then those cards are removed from
        the player's hand and put into the books attribute.
        """
        for rank, suits in self.state.items():
            if len(suits) == 4:
                self.books.append(rank)

                # remove cards of rank from hand
                self.hand = [c for c in self.hand if c.rank != rank]

    def ask(self, another_player, rank):
        """ask another player if they have a card of a particular rank"""
        cards = another_player.tell(rank)

        obtained_card = cards

        self.receive(cards)

        self.check_for_books()

        return obtained_card

    def tell(self, rank):
        """give card to another player if they have a card of requested rank"""
        # get indicies of instances of card
        idx = [i for i, c in enumerate(self.hand) if rank in str(c)]

        cards_to_give = [self.hand[i] for i in idx]

        self.remove(cards_to_give)

        return cards_to_give
