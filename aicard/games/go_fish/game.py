from aicard.games.go_fish.states import GoFishState
from aicard.games.go_fish import GO_FISH_INITIAL_HAND_SIZE_MAP


class GoFishGame:
    """A class for executing a game of Go Fish.

    Note: 
        The state includes players and players observations as well as
        a map which maps a play index to a list of indices of that players's
        opponents.
    """
    # ALlowed suits
    ALLOWED_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    # Allowed ranks
    ALLOWED_RANKS = ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King']
    def __init__(self, num_players):
        self.num_players = num_players
        self.state = GoFishState(self.num_players)
        self.turn = 1

    def deal(self):
        """Deal cards to players."""
        print(f"Dealing cards to players.\n")
        # Shuffle deck to ensure random start
        self.state.deck.shuffle()

        # all players take draw cards initial hand size attained.
        for _ in range(GO_FISH_INITIAL_HAND_SIZE_MAP[self.num_players]):
            for index, player in self.state.players:
                player.draw(self.state.deck)

    def turn(self):
        print(f'Beginning Turn {self.turn}.\n')
        for index, player in self.state.players:
            print(f"Player {index+1} of {self.num_players} is beginning their turn.\n")
            self.player_turn(player)

    def player_turn(self, player):
        """Player asks opponent for a card and goes fish if no exchange."""
        deck = self.deck

        # If players holds no cards, they may draw a card if there are cards remaining in the deck.
        if len(player.hand) == 0:
            if len(deck.cards) > 0:
                player.draw(deck)

        # a players may ask for a card if they have at least one card.
        keep_asking = len(player.hand) > 0

        # a players may keep asking for cards as long as they recieve a card from an opponent.
        asks = 0
        while keep_asking:
            # use policies to choose action
            policy = GoFishRandomPolicy(observation, valid_actions)
            action = policy.sample()
            
            ask_index = action[0]  # index of players to ask for a card.
            ask_rank = action[1]  # rank of card to ask for.

            print(f"{player.name} is asking for a {ask_rank}")
            keep_asking = player.ask(opponent, ask_rank)
            asks += 1
            if keep_asking:
                print(f"{player.name} obtained at least one {ask_rank} from {opponent.name}.")
            else:
                print(f"{player.name} did not obtain a {ask_rank} from {opponent.name}.")

            if len(player.hand) == 0:
                if len(deck.cards) > 0:
                    player.draw(deck)
                else:
                    keep_asking = False

        if len(deck.cards) == 0:
            print(f"The Deck is empty.")
        elif asks == 1:
            print(f"{player.name} is drawing a card.")
            player.draw(deck)
