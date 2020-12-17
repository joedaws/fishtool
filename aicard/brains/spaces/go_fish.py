from aicard.games.core import ALLOWED_RANKS
from aicard.games.core.events import ExchangeEvent, BookEvent
from aicard.games.go_fish import GO_FISH_INITIAL_HAND_SIZE_MAP


class ObservedRanks:
    """Class for storing observations about ranks passed by other players."""
    def __init__(self, opponents):
        self.num_opponents = len(opponents)
        self.ranks = {i: {rank: 0 for rank in ALLOWED_RANKS} for i in opponents}

    def update(self, event):
        """After an event update the observed ranks.

        Args:
            event: Either ExchangeEvent or BookEvent.
        """
        if isinstance(event, ExchangeEvent):
            self.update_exchange_event(event)
        elif isinstance(event, BookEvent):
            self.update_book_event(event)
        elif isinstance(event, AskEvent):
            self.update_ask_event(event)
        else:
            raise ValueError(f'Cannot update observed ranks for event type {type(event)}')

    def update_exchange_event(self, exchange_event):
        """Update the observed ranks after a witnessed event.

        Args:
            exchange_event (EchangeEvent): A dataclass including, player_giving_index,
                player_receiving_index, rank, number.
        """
        # decrease known ammount of rank of the giving players
        number = exchange_event.number
        giving_player = self.ranks[exchange_event.player_giving]
        giving_player[exchange_event.rank] = min(number-giving_player[exchange_event.rank], 0)

        # increase the known amount of rank of the receiving players
        receiving_player = self.ranks[exchange_event.player_receiving]
        receiving_player[exchange_event.rank] += number

    def update_book_event(self, book_event):
        """Update the observed ranks after a book event.

        """
        # TODO: fill in this method.
        pass

    def update_ask_event(self, ask_event):
        """Update the observed ranks after an ask event."""
        self.ranks[ask_event.player][ask_event.rank] += 1


class ObservedHandLen:
    """Class for storing observations about the number fo cards possed by other players."""
    INITIAL_HAND_SIZE_M5P = {2: 7, 3: 7, 4: 5, 5: 5}

    def __init__(self, opponents):
        self.num_opponents = len(opponents)
        self.opponents = opponents
        self.hand_len = {i: GO_FISH_INITIAL_HAND_SIZE_MAP[self.num_opponents]
                         for i in self.opponents}

    def valid_opponents(self):
        """Return list of indices corresponding to opponents with at least one card."""
        return [i for i in self.opponents if self.hand_len[i] > 0]

    def update(self, event):
        """After an event update the number of cards in a hand.

        Args:
            event: Either ExchangeEvent or BookEvent.
        """
        if isinstance(event, ExchangeEvent):
            self.update_exchange_event(event)
        elif isinstance(event, BookEvent):
            self.update_book_event(event)
        elif isinstance(event, DrawEvent):
            self.update_draw_event(event)
        else:
            raise ValueError(f'Cannot update observed ranks for event type {type(event)}')

    def update_exchange_event(self, exchange_event):
        """Update the number of cards in hands after a witnessed event.

        Args:
            exchange_event (EchangeEvent): A dataclass including, player_giving_index,
                player_receiving_index, rank, number.
        """
        number = exchange_event.number

        # decrease giving players's count
        self.hand_len[exchange_event.player_giving_index] -= number

        # increate receiving players's count
        self.hand_len[exchange_event.player_receiving_index] += number

    def update_book_event(self, book_event):
        """Update the number of cards in hands after a book event."""
        self.hand_len[book_event.player] -= 4

    def update_draw_event(self, draw_event):
        """Update the number of cards in hands after a draw event."""
        number = draw_event.number
        self.hand_len[draw_event.player] += number


class ObservationSpace:
    """Go Fish observation spaces."""
    def __init__(self, opponents):
        self.opponents = opponents
        self.num_opponents = len(opponents)
        self.observed_ranks = ObservedRanks(self.opponents)
        self.observed_hand_len = ObservedHandLen(self.opponents)

    def get_observation(self):
        """Return a tuple representing the observation by a players."""
        ranks = self.observed_ranks.ranks
        lens = self.observed_hand_len.hand_len
        return (ranks, lens)

    def update(self, event):
        """Update the observation spaces based on observed event."""
        self.observed_ranks.update(event)
        #update opponents hand lengths
        self.observed_hand_len.update(event)

class ActionSpace:
    """Go Fish action spaces"""
    def __init__(self, num_opponents):
        self.num_opponents = num_opponents
        self.opponents = tuple(i for i in range(num_opponents))

    @property
    def valid_ranks(self):
        return 1

    @property
    def valid_opponents(self):
        """Returns list of opponents whom the players can ask a card from.
        
        You can only as an opponent for cards if they have cards to ask for.
        """



