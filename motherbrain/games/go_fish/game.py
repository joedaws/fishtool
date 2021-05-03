"""
Game: GoFish
Policies: Human, random
Animators: Text
"""
from motherbrain.games.go_fish.state import GoFishState
from motherbrain.games.go_fish.state import GoFishStateObserver
from motherbrain.games.go_fish import INITIAL_HAND_SIZE_MAP
from motherbrain.brains.spaces.go_fish.actions import Actions
from motherbrain.players.go_fish import GoFishPlayer
from motherbrain.games.core.game import Game
from motherbrain.games.core.events import DrawEvent, \
                                     BookEvent, \
                                     AskEvent, \
                                     FailEvent, \
                                     SuccessEvent, \
                                     ExchangeEvent, \
                                     RemovePlayerEvent


class GoFishGame(Game):
    """A class for executing a game of Go Fish.

    Note:
        The state includes players and players observations as well as
        a map which maps a play index to a list of indices of that players's
        opponents.

        The kind of text animation used depends on whether or not a human
        policy is being used.

    Args:
        policies (list): A list of policy classes.
    """
    # total number of books, this number is used to determine termination conditions.
    TOTAL_BOOKS = 13
    NAME = 'Go Fish!'

    def __init__(self, policies):
        self.num_players = len(policies)

        # initialize game state
        self.state = GoFishState(self.num_players)

        # attach game state observers
        # TODO make this conditional so that you don't always have an observer
        game_state_observer = GoFishStateObserver()
        self.state.attach(game_state_observer)
        
        # initialize turn number
        self.turn_number = 1

        # instantiate a policy for each player
        self.policies_map = {player: policy()
                             for policy, player in zip(policies, self.state.players)}

        # initialize 
        self.over = False

        # set up print based on which policies are being used to choose actions
        self.print_method = None
        self._setup_print_method(policies)

    def play(self):
        """Play a game of Go Fish."""
        self.deal()
        while not self.over:
            self.turn()

        # record collected game data
        for observer in self.state._observers:
            observer.record_history()

    def deal(self):
        """Deal cards to players."""
        #print(f"PHASE: begin dealing phase.\n\n")
        # Shuffle deck to ensure random start
        self.state.deck.shuffle()

        # all players take draw cards initial hand size attained.
        for _ in range(INITIAL_HAND_SIZE_MAP[self.num_players]):
            for player in self.state.players:
                draw, book = self.event_draw(player)
                self.state.update(draw)
                self.state.update(book)

        self.print_method(f"The cards have been dealt! BEGIN!\n")

    def turn(self):
        """Execute a full turn."""
        self.print_method(f'Beginning Turn {self.turn_number}.')
        for player in self.state.players:
            # if a player is out they don't play their turn.
            if not player.is_out:
                self.print_method(f"{player.name} is beginning their turn.\n")
                self.player_turn(player)
            self.check_game_over()

            # no need to have the other players take their turn.
            if self.over:
                break

        self.print_method(f'After Turn {self.turn_number} the status is. . .')
        status_str = ""
        for player in self.state.players:
            
            status_str = f"{player.name} has {len(player.books)}"\
                         f" books and {len(player.hand)} cards."
            self.print_method(status_str)

        deck_status_str = f"The deck has {len(self.state.deck.cards)} cards remaining."
        self.print_method(deck_status_str)

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
                self.print_method(f"{player.name} made a book with rank {book.rank}.")

        if isinstance(card_check, FailEvent) and len(self.state.deck.cards) == 0:
            self.print_method(f"{player.name} is out!")
            remove_player = self.event_remove_player(player)
            self.state.update(remove_player)

        # a players may keep asking for cards as long as they receive a card from an opponent.
        asks = 0
        while keep_asking:
            # ensure player has cards before asking. Remove them if they do not.
            card_check = self.event_has_cards(player)
            if isinstance(card_check, FailEvent) and len(self.state.deck.cards) == 0:
                self.print_method(f"{player.name} is out!")
                remove_player = self.event_remove_player(player)
                self.state.update(remove_player)
                break

            # get available actions
            observations = self.state.observations[player]
            actions = Actions(observations=observations, hand=player.hand)

            # give available actions to policy and choose an action
            policy = self.policies_map[player]
            policy.actions = actions
            policy.observations = observations
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
                    self.print_method(f"{player.name} obtained a {exchange.rank} from {opponent.name}.")
                else:
                    self.print_method(f"{player.name} obtained {exchange.number} {exchange.rank}s from {opponent.name}.")

            elif isinstance(exchange, FailEvent):
                self.print_method(f"{player.name} did not obtain a {ask_rank} from {opponent.name}.")
                # A player who does not make a catch cannot keep asking.
                keep_asking = False

            # print statements about books
            if isinstance(book, BookEvent):
                self.print_method(f"{player.name} made a book with rank {book.rank}.")

        if not player.is_out:
            # after the asking phase of the turn ends, the player draws a card.
            draw, book = self.event_draw(player)
            self.state.update(draw)
            self.state.update(book)
            if isinstance(book, BookEvent):
                self.print_method(f"{player.name} made a book with rank {book.rank}.")

            # print statement about end of player's turn
            self.print_method(f"{player.name} has finished their turn.\n")

    def event_draw(self, player: GoFishPlayer):
        """Draw a card from the deck and generate a DrawEvent."""
        deck = self.state.deck
        if len(deck) > 0:
            draw, book = player.draw(deck)
            self.print_method(f"{player.name} drew a card from the deck and now has {len(player.hand)} card(s).")
        else:
            self.print_method(f"{player.name} tried to draw a card, but the deck was empty.")
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

    def event_ask(self, rank: str, player: GoFishPlayer, opponent: GoFishPlayer):
        """Generate an AskEvent based on the player."""
        self.print_method(f"{player.name} is asking {opponent.name} for a {rank}.")
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
                self.print_method(f"{type(policy)} cannot or does not need to be reset.")

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
            self.print_method(f"All books are acquired. {winner} has won!")

    @staticmethod
    def get_player_state_str(player):
        """returns string representation of a players state"""
        state_str = f"{player.name} state:"
        for rank in player.state:
            if player.state[rank]:
                state_str += rank + ": "
            for suit in player.state[rank]:
                state_str += suit + " "
            if player.state[rank]:
                state_str += " "

        return state_str

    def get_state_str(self):
        """Returns string representation of the state."""
        state_str = f"The state of the go fish game:"
        for player in self.state.players:
            state_str += self.get_player_state_str(player)

        return state_str

    def __str__(self):
        """Printable version of state of Game."""
        state_str = self.get_state_str()
        return state_str

    def _setup_print_method(self, policies):
        """Chooses the appropriate TextAnimator based on the policies playing.

        When a human policy is used, use the slow text animator.
        This method choose the "strategy" for printing text.

        Args:
            policies (list): List of policies being used in the
                game to choose actions.
        """
        # check policies for human policy
        policy_names = [policy.NAME for policy in policies]
        if 'human' in policy_names:
            # set print strategy to slow text
            from motherbrain.engine.animators.slow_text import SlowText
            st = SlowText()
            self.print_method = st.animate_text

        else: 
            # set print strategy to fast text
            self.print_method = print

