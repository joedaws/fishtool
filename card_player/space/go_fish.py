from card_player.deck import ALLOWED_RANKS
from card_player.game import ExchangeEvent, BookEvent
from card_player.game import GO_FISH_INITIAL_HAND_SIZE_MAP as INITIAL_HAND_SIZE_MAP


class ObservedRanks:
    """Class for storing observations about ranks possed by other players."""
    def __init__(self, opponents):
        self.num_opponents = len(opponents)
        self.observed_ranks = {i: {rank: 0 for rank in ALLOWED_RANKS} for i in opponents}

    def update(self, event):
        """After an event update the observed ranks.

        Args:
            event: Either ExchangeEvent or BookEvent.
        """
        if isinstance(event, ExchangeEvent):
            self.update_exchange_event(event)
        elif isinstance(event, BookEvent):
            self.update_book_event(event)
        else:
            raise ValueError(f'Cannot update observed ranks for event type {type(event)}')

    def update_exchange_event(self, exchange_event):
        """Update the observed ranks after a witnessed event.

        Args:
            exchange_event (EchangeEvent): A dataclass including, player_giving_index,
                player_receiving_index, rank, number.
        """
        # decrease known ammount of rank of the giving player
        number = exchange_event.number
        giving_player = self.observed_ranks[exchange_event.player_giving]
        giving_player[exchange_event.rank] = min(number-giving_player[exchange_event.rank], 0)

        # increase the known amount of rank of the receiving player
        receiving_player = self.observed_ranks[exchange_event.player_receiving]
        receiving_player[exchange_event.rank] += number

    def update_book_event(self, book_event):
        """Update the observed ranks after a book event.

        """
        # TODO: fill in this method.
        pass

class ObservedHandLen:
    """Class for storing observations about the number fo cards possed by other players."""
    def __init__(self, opponents):
        self.num_opponents = len(opponents)
        self.hand_len = {i: INITIAL_HAND_SIZE_MAP[self.num_opponents]
                         for i in self.opponents}

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

        # decrease giving player's count
        self.hand_len[exchange_event.player_giving_index] -= number

        # increate receiving player's count
        self.hand_len[exchange_event.player_receiving_index] += number

    def update_book_event(self, book_event):
        """Update the number of cards in hands after a book event."""
        self.hand_len[book_event.player] -= 4

    def update_draw_event(self, draw_event):
        """Update the number of cards in hands after a draw event."""
        number = draw_event.number
        self.hand_len[draw_event.player] += number

class ObservationSpace:
    """Go Fish observation space."""
    def __init__(self, opponents):
        self.opponents = opponents
        self.num_opponents = len(opponents)
        self.observed_ranks = ObservedRanks(self.opponents)
        self._opponents_hand_len = None

    @property
    def opponents_hand_len(self):
        """Returns a dictionary whose keys are opponent indicies and
        keys are number of cards the corresponding opponents hand."""
        if self._opponents_hand_len is None:
            # initialize to default hand size
            self._opponents_hand_len = {i: INITIAL_HAND_SIZE_MAP[self.num_opponents]
                                        for i in self.opponents}

        return self._opponents_hand_len

    @property
    def valid_opponents(self):
        """Returns tuple of indices of opponents with cards."""
        return tuple(i for i in self.opponents if self.opponents_hand_len[i] > 0)

    def update(self, event):
        """Update the observation space based on observed event."""
        self.observed_ranks.update(event)
        #update opponents hand lengths
        self.update_opponents_hand_len()

    def update_opponents_hand_len(self, event):


class ActionSpace:
    """Go Fish action space"""
    def __init__(self, num_opponents):
        self.num_opponents = num_opponents
        self.opponents = tuple(i for i in range(num_opponents))

    @property
    def valid_ranks(self):
        return 1

    @property
    def valid_opponents(self):
        """Returns list of opponents whom the player can ask a card from.
        
        You can only as an opponent for cards if they have cards to ask for.
        """



