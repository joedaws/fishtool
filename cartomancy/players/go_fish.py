from cartomancy.players.base import Player
from cartomancy.games.go_fish.card import CARD_FIELD_VALUES
from cartomancy.games.core.events import ExchangeEvent, BookEvent, FailEvent, DrawEvent


ALLOWED_RANKS = CARD_FIELD_VALUES['rank']


class GoFishPlayer(Player):
    """A go Fish players class."""
    GAME = 'GoFish'

    def __init__(self, name):
        super().__init__(name)
        self.books = []
        self.is_out = False

    @property
    def state(self):
        """A dictionary for describing contents of hand.

        The keys are the allowed ranks that the players current
        has in their hand and the values are lists
        of suits of the cards of that rank.
        """
        if self.hand is None:
            raise ValueError(f'Cannot compute state for uninitialized hand.')

        state = {rank: [] for rank in ALLOWED_RANKS}

        for card in self.hand:
            state[card.rank].append(card.suit)

        return state

    def look_for_rank_match(self, rank):
        """Find all cards in hand matching a given rank"""
        if rank not in ALLOWED_RANKS:
            raise ValueError(f'{rank} is not a valid rank.')

        rank_matched_cards = [card for card in self.hand if card.rank == rank]

        return rank_matched_cards

    def _check_for_books(self):
        """Check hand for books.

        If a book is found then those cards are removed from
        the players's hand and put into the books attribute.

        Since we check for books after each time this player obtains new
        cards of one rank, there can only be at most one book.
        """
        event = None
        for rank, suits in self.state.items():
            if len(suits) == 4:
                self.books.append(rank)

                # create book event
                event = BookEvent(player=self, rank=rank)

                # remove cards of rank from hand
                self.hand = [c for c in self.hand if c.rank != rank]

                break  # book was found and there can only be one book during this check.

        if event is None:
            # create fail event since no book was made
            event = FailEvent(player=self)

        return event

    def ask(self, another_player, rank):
        """ask another players if they have a card of a particular rank.

        Returns two events based on what occured during the execution.
        If the other player gives cards, then an Exchanged event is created.
        If the other player gives no cards, then a fail event is created.
        If this player makes a book after receiving cards, then a BookEvent is created.
        If this player makes does not make a book after receiving cards, then a fail
        event is created.

        Returns:
            Event based on the outcome of the ask
            Event based on the outcome of the checking for books
        """
        cards = another_player.tell(rank)

        self.receive(cards)

        if cards:
            exchange = ExchangeEvent(source=self, destination=another_player, rank=rank, number=len(cards))
        else:
            exchange = FailEvent(player=self)

        book = self._check_for_books()

        return exchange, book

    def draw(self, deck, n=1):
        """Player draws card(s) from provided deck.

        Args:
            deck (Deck): A instance of a card deck.
            n (int): Number of cards to draw from the deck.
        """
        new_cards = [deck.draw(1)[0] for _ in range(n)]

        self.receive(new_cards)

        draw = DrawEvent(player=self, number=n)

        book = self._check_for_books()

        return draw, book

    def tell(self, rank):
        """give card to another players if they have a card of requested rank"""
        # get indices of instances of card
        idx = [i for i, c in enumerate(self.hand) if rank in str(c)]

        cards_to_give = [self.hand[i] for i in idx]

        self.remove(cards_to_give)

        return cards_to_give
