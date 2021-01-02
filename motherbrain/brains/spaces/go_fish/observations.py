from motherbrain.games.go_fish.card import CARD_FIELD_VALUES
from motherbrain.games.core.events import ExchangeEvent, BookEvent, AskEvent, DrawEvent, FailEvent, SuccessEvent


ALLOWED_RANKS = CARD_FIELD_VALUES['rank']


class ObservedOpponentRanks:
    """Class for storing observations about ranks possessed by an opponent.

    Args:
        opponent (GoFishPlayer): A  player instance that is an opponent.
    """
    def __init__(self, opponent):
        self.opponent = opponent
        self.ranks = {rank: 0 for rank in ALLOWED_RANKS}

    def update(self, event):
        """After an event update the observed ranks.

        Args:
            event: A dataclass from motherbrain.games.core.events
        """
        if isinstance(event, ExchangeEvent):
            self.update_exchange_event(event)
        elif isinstance(event, BookEvent):
            self.update_book_event(event)
        elif isinstance(event, AskEvent):
            self.update_ask_event(event)
        else:
            # raise ValueError(f'Cannot update observed ranks for event type {type(event)}')
            pass

    def update_exchange_event(self, exchange_event):
        """Update the observed ranks after a witnessed event.

        The exchange event either increase the observed count of rank or decreases it.

        Args:
            exchange_event (ExchangeEvent): A dataclass including, player_giving,
                player_receiving, rank, number.
        """
        if self.opponent == exchange_event.destination:
            self.ranks[exchange_event.rank] += exchange_event.number

        elif self.opponent == exchange_event.source:
            self.ranks[exchange_event.rank] = 0

    def update_book_event(self, book_event):
        """Update the observed ranks after a book event."""
        if self.opponent == book_event.player:
            self.ranks[book_event.rank] = 0

    def update_ask_event(self, ask_event):
        """Update the observed ranks after an ask event."""
        if self.opponent == ask_event.player:
            self.ranks[ask_event.rank] += 1


class ExactOpponentHandLen:
    """Class for storing the exact hand lengths of opponents."""
    def __init__(self, opponent):
        self.opponent = opponent

    @property
    def hand_len(self):
        """Returns true hand length of opponent."""
        return len(self.opponent.hand)

    @property
    def is_valid(self):
        """Boolean for is hand_len is non-zero."""
        return self.hand_len > 0

    def update(self, event):
        """We can ignore all events in this case."""
        pass


class ObservedOpponentHandLen:
    """Class for storing observations about the number of cards possessed by an opponent."""
    def __init__(self, opponent):
        self.opponent = opponent
        self.hand_len = 0

    @property
    def is_valid(self):
        """Boolean for is hand_len is non-zero."""
        return self.hand_len > 0

    def update(self, event):
        """After an event update the number of cards in a hand.

        Args:
            event: Either ExchangeEvent or BookEvent.
        """
        if isinstance(event, ExchangeEvent):
            self.update_exchange_event(event)
        elif isinstance(event, DrawEvent):
            self.update_draw_event(event)
        elif isinstance(event, BookEvent):
            self.update_book_event(event)
        else:
            #  raise ValueError(f'Cannot update observed ranks for event type {type(event)}')
            pass

    def update_exchange_event(self, exchange_event):
        """Update the number of cards in hands after a witnessed event.

        Args:
            exchange_event (EchangeEvent): A dataclass including, player_giving_index,
                player_receiving_index, rank, number.
        """
        if self.opponent == exchange_event.destination:
            self.hand_len += exchange_event.number

        elif self.opponent == exchange_event.source:
            self.hand_len -= exchange_event.number

    def update_book_event(self, book_event):
        """Update the number of cards in hands after a book event."""
        if self.opponent == book_event.player:
            self.hand_len -= 4

    def update_draw_event(self, draw_event):
        """Update the number of cards in hands after a draw event."""
        if self.opponent == draw_event.player:
            self.hand_len += 1


class Observations:
    """Go Fish observation spaces.

    Holds data known to a particular player about the state of the game and the
    partially known information about the opponents.
    """
    def __init__(self, player, opponents):
        self.player = player
        self.opponents = opponents
        self.num_opponents = len(opponents)
        self.observed_ranks = {opponent: ObservedOpponentRanks(opponent) for opponent in self.opponents}
        self.observed_hand_len = {opponent: ExactOpponentHandLen(opponent) for opponent in self.opponents}

    def get_observation(self, opponent):
        """Return a tuple representing the observation by a players."""
        ranks = self.observed_ranks[opponent].ranks  # a dictionary whose keys are ranks
        number = self.observed_hand_len[opponent].hand_len  # an integer describing number of cards
        return ranks, number

    def update(self, event):
        """Update the observation spaces based on observed event."""
        for opponent in self.opponents:
            self.observed_ranks[opponent].update(event)
            self.observed_hand_len[opponent].update(event)
