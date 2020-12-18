from aicard.games.go_fish.states import GoFishState
from aicard.games.core.events import DrawEvent, BookEvent, AskEvent, FailEvent, SuccessEvent, ExchangeEvent
from aicard.games.go_fish import GO_FISH_INITIAL_HAND_SIZE_MAP
from aicard.brains.policies.go_fish.random import GoFishRandomPolicy
from aicard.brains.spaces.go_fish.actions import Actions
from aicard.brains.spaces.go_fish.observations import Observations
from aicard.players.go_fish import GoFishPlayer


class GoFishGame:
    """A class for executing a game of Go Fish.

    Note: 
        The state includes players and players observations as well as
        a map which maps a play index to a list of indices of that players's
        opponents.
    """
    def __init__(self, num_players):
        self.num_players = num_players
        self.state = GoFishState(self.num_players)
        self.turn = 1
        # self.policies = {player: GoFishRandomPolicy() for player in self.state.players}

    def deal(self):
        """Deal cards to players."""
        print(f"\nPHASE: begin dealing phase.\n")
        # Shuffle deck to ensure random start
        self.state.deck.shuffle()

        # all players take draw cards initial hand size attained.
        for _ in range(GO_FISH_INITIAL_HAND_SIZE_MAP[self.num_players]):
            for player in self.state.players:
                draw, book = self.event_draw(player)
                self.state.update(draw)
                self.state.update(book)

        print(f"\nPHASE: End dealing phase.\n")

    def turn(self):
        print(f'Beginning Turn {self.turn}.\n')
        for player in self.state.players:
            print(f"Player {player.index} of {self.num_players} is beginning their turn.\n")
            self.player_turn(player)

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

        # a players may keep asking for cards as long as they receive a card from an opponent.
        asks = 0
        while keep_asking:
            # get available actions
            observations = self.state.observations[player]
            actions = Actions(observations=observations, hand=player.hand)

            # use policies to choose action
            policy = GoFishRandomPolicy(actions=actions)
            ask_index, ask_rank = policy.sample()
            opponent = self.state.opponents_map[player][ask_index]

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
    def event_ask(ask_rank: str, player: GoFishPlayer, opponent: GoFishPlayer):
        """Generate an AskEvent based on the player."""
        print(f"{player.name} is asking {opponent.name} for a {ask_rank}.")
        event = AskEvent(player=player, opponent=opoonent, ask_rank=ask_rank)
        return event

    @staticmethod
    def event_exchange(ask_event: AskEvent):
        """Generate and perform an ExchangeEvent based on ask event."""
        ask_rank = ask_event.rank
        player = ask_event.player
        opponent = ask_event.opponent
        cards = player.ask(opponent, ask_rank)
        if cards:
            event = ExchangeEvent(player_receiving=player, player_giving=opponent, rank=ask_rank, number=len(cards))
        else:
            event = FailEvent(player=player)

        return event
