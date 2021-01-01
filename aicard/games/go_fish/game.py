from aicard.games.go_fish.state import GoFishState
from aicard.games.go_fish import INITIAL_HAND_SIZE_MAP
from aicard.brains.spaces.go_fish.actions import Actions
from aicard.players.go_fish import GoFishPlayer
from aicard.games.core.events import DrawEvent, \
                                     BookEvent, \
                                     AskEvent, \
                                     FailEvent, \
                                     SuccessEvent, \
                                     ExchangeEvent, \
                                     RemovePlayerEvent


class GoFishGame:
    """A class for executing a game of Go Fish.

    Note:
        The state includes players and players observations as well as
        a map which maps a play index to a list of indices of that players's
        opponents.

    Args:
        policies (list): A list of policy classes.
    """
    # total number of books, this number is used to determine termination conditions.
    TOTAL_BOOKS = 13     
    NAME = 'Go Fish!'

    def __init__(self, policies):
        self.num_players = len(policies)
        self.state = GoFishState(self.num_players)
        self.turn_number = 1
        # instantiate a policy for each player
        self.policies_map = {player: policy()
                             for policy, player in zip(policies, self.state.players)}

        self.over = False

    def play(self):
        """Play a game of Go Fish."""
        self.deal()
        while not self.over:
            self.turn()

    def deal(self):
        """Deal cards to players."""
        print(f"\nPHASE: begin dealing phase.\n")
        # Shuffle deck to ensure random start
        self.state.deck.shuffle()

        # all players take draw cards initial hand size attained.
        for _ in range(INITIAL_HAND_SIZE_MAP[self.num_players]):
            for player in self.state.players:
                draw, book = self.event_draw(player)
                self.state.update(draw)
                self.state.update(book)

        print(f"\nPHASE: End dealing phase.\n")

    def turn(self):
        print(f'\nBeginning Turn {self.turn_number}.')
        for player in self.state.players:
            # if a player is out they don't play their turn.
            if not player.is_out:
                print(f"\n{player.name} is beginning their turn.\n")
                self.player_turn(player)
            self.check_game_over()

            # no need to have the other players take their turn.
            if self.over:
                break

        print(f'\nAfter Turn {self.turn_number} the status is. . .')
        status_str = ""
        for player in self.state.players:
            status_str += f"{player.name} has {len(player.books)}"\
                          f" books and {len(player.hand)} cards.\n"
        status_str += f"The deck has {len(self.state.deck.cards)} cards remaining."
        print(status_str)

        self.turn_number += 1

    def player_turn(self, player: GoFishPlayer):
        """Player asks opponent for a card and goes fish if no exchange."""
        # If players holds no cards, they may draw a card if there are cards remaining in the deck.
        card_check = self.event_has_cards(player)
        keep_asking = isinstance(card_check, SuccessEvent)

        if isinstance(card_check, FailEvent):
            draw, book = self.event_draw(player)
            self.state.update(draw)
            self.state.update(book)
            keep_asking = isinstance(draw, DrawEvent)
            # print statements about books
            if isinstance(book, BookEvent):
                print(f"{player.name} made a book with rank {book.rank}.")

        if isinstance(card_check, FailEvent) and len(self.state.deck.cards) == 0:
            print(f"{player.name} is out!")
            remove_player = self.event_remove_player(player)
            self.state.update(remove_player)

        # a players may keep asking for cards as long as they receive a card from an opponent.
        asks = 0
        while keep_asking:
            # ensure player has cards before asking. Remove them if they do not.
            card_check = self.event_has_cards(player)
            if isinstance(card_check, FailEvent) and len(self.state.deck.cards) == 0:
                print(f"{player.name} is out!")
                remove_player = self.event_remove_player(player)
                self.state.update(remove_player)
                break

            # get available actions
            observations = self.state.observations[player]
            actions = Actions(observations=observations, hand=player.hand)

            # give available actions to policy and choose an action
            policy = self.policies_map[player]
            policy.actions = actions
            opponent, ask_rank = policy.sample()

            # generate ask event
            ask = self.event_ask(ask_rank, player, opponent)
            self.state.update(ask)

            exchange, book = player.ask(opponent, ask_rank)
            self.state.update(exchange)
            self.state.update(book)

            asks += 1
            # print statements about exchange
            if isinstance(exchange, ExchangeEvent):
                if exchange.number == 1:
                    print(f"{player.name} obtained a {exchange.rank} from {opponent.name}.")
                else:
                    print(f"{player.name} obtained {exchange.number} {exchange.rank}s from {opponent.name}.")

            elif isinstance(exchange, FailEvent):
                print(f"{player.name} did not obtain a {ask_rank} from {opponent.name}.")
                # A player who does not make a catch cannot keep asking.
                keep_asking = False

            # print statements about books
            if isinstance(book, BookEvent):
                print(f"{player.name} made a book with rank {book.rank}.")

        if not player.is_out:
            # after the asking phase of the turn ends, the player draws a card.
            draw, book = self.event_draw(player)
            self.state.update(draw)
            self.state.update(book)
            if isinstance(book, BookEvent):
                print(f"{player.name} made a book with rank {book.rank}.")

            # print statement about end of player's turn
            print(f"{player.name} has finished their turn.")

    def event_draw(self, player: GoFishPlayer):
        """Draw a card from the deck and generate a DrawEvent."""
        deck = self.state.deck
        if len(deck) > 0:
            draw, book = player.draw(deck)
            print(f"{player.name} drew a card from the deck and now has {len(player.hand)} card(s).")
        else:
            print(f"{player.name} tried to draw a card, but the deck was empty.")
            draw = FailEvent(player=player)
            book = FailEvent(player=player)

        return draw, book

    @staticmethod
    def event_has_cards(player: GoFishPlayer):
        """Generate a SuccessEvent if player has cards in hand."""
        if len(player.hand) > 0:
            event = SuccessEvent(player)
        else:
            event = FailEvent(player)

        return event

    @staticmethod
    def event_ask(rank: str, player: GoFishPlayer, opponent: GoFishPlayer):
        """Generate an AskEvent based on the player."""
        print(f"{player.name} is asking {opponent.name} for a {rank}.")
        event = AskEvent(player=player, opponent=opponent, rank=rank)
        return event

    @staticmethod
    def event_exchange(ask_event: AskEvent):
        """Generate and perform an ExchangeEvent based on ask event."""
        ask_rank = ask_event.rank
        player = ask_event.player
        opponent = ask_event.opponent
        cards = player.ask(opponent, ask_rank)
        if cards:
            event = ExchangeEvent(player_receiving=player,
                                  player_giving=opponent,
                                  rank=ask_rank,
                                  number=len(cards))
        else:
            event = FailEvent(player=player)

        return event

    @staticmethod
    def event_remove_player(player: GoFishPlayer):
        """Generate remove player event."""
        player.is_out = True
        event = RemovePlayerEvent(player)
        return event

    def reset(self):
        """reset to beginning of game."""
        self.state.reset()
        self.turn_number = 1
        # try to reset policies
        for _, policy in self.policies_map.items():
            try:
                policy.reset()
            except AttributeError:
                print(f"{type(policy)} cannot or does not need to be reset.")

        # reset game over flag
        self.over = False

    def check_game_over(self):
        """See if the game is over."""
        total_books = 0
        for player in self.state.players:
            total_books += len(player.books)

        self.over = total_books == self.TOTAL_BOOKS

        if self.over:
            book_totals = {len(player.books): player
                           for player in self.state.players}
            winner = book_totals[max(book_totals)].name
            print(f"\nAll books are acquired. {winner} has won!")

    @staticmethod
    def get_player_state_str(player):
        """returns string representation of a players state"""
        state_str = f"{player.name} state:\n"
        for rank in player.state:
            if player.state[rank]:
                state_str += rank + ": "
            for suit in player.state[rank]:
                state_str += suit + " "
            if player.state[rank]:
                state_str += "\n"

        return state_str

    def get_state_str(self):
        """Returns string representation of the state."""
        state_str = f"The state of the go fish game:\n"
        for player in self.state.players:
            state_str += self.get_player_state_str(player)

        return state_str

    def __str__(self):
        """Printable version of state of Game."""
        state_str = self.get_state_str()
        return state_str

