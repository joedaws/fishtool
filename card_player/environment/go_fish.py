import gym
from gym import spaces
from gym.utils import seeding
from card_player.deck import ALLOWED_RANKS
from card_player.game import ExchangeEvent


class ObservedRanks:
    """Class for storing observations about ranks possed by other players"""
    def __init__(self, opponents):
        self.num_opponents = len(opponents)
        self.observed_ranks = {i: {rank: 0 for rank in ALLOWED_RANKS} for i in opponents}

    def update_observed_ranks_book_event(self, event):
        if isinstance(event, ExchangeEvent):
            self.update_observed_ranks_exchange_event(event)
        else:
            raise ValueError(f'Cannot update observed ranks for event type {type(event)}')

    def update_observed_ranks_exchange_event(self, exchange_event):
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


class ObservationSpace:
    """Go Fish observation space"""
    NUM_RANKS = 13
    def __init__(self, num_opponents, initial_hand_size):
        self.num_opponents = num_opponents
        self.opponents = tuple(i for i in range(num_opponents))
        self.opponents_hand_len = {i: initial_hand_size for i in self.opponents}
        self.ranks = tuple(i for i in range(self.NUM_RANKS))
        self.opponent_rank = {i:{} for i in self.opponents}

    @property
    def valid_opponents(self):
        """Returns tuple of indices of opponents with cards."""
        return tuple(i for i in self.opponents if self.opponents_hand_len[i] > 0)

    @property
    def known_ranks(self):
        """Returns dictionary of ranks """
        known_ranks = 0
        return known_ranks

class GoFIshEnv(gym.Env):
    """Go Fish environment implementation.

    Action Space:
        Each player may ask for one of the ranks from one of the players.
        Therefore, the action space is a tuple with the number of players
        and a discrete space of 13 (the total number of ranks).

    Observation Space:
        Each player

    Args:
        num_oppoents (int): number of OTHER players that will play the game.
    """
    NUM_RANKS = 13  # total number of ranks that a card may have.
    def __init__(self, num_opponents):
        self.action_space = spaces.Tuple((
            spaces.Discrete(num_opponents), 
            spaces.Discrete(self.NUM_RANKS)
            ))
        
        self.observation_space = spaces.Tuple((
            spaces.Discrete
            ))
        self.observation_space = spaces.Tuple((
            spaces.Discrete(32),
            spaces.Discrete(11),
            spaces.Discrete(2)))
        self.seed()

        # Flag to payout 1.5 on a "natural" blackjack win, like casino rules
        # Ref: http://www.bicyclecards.com/how-to-play/blackjack/
        self.natural = natural
        # Start the first game
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        if action:  # hit: add a card to players hand and return
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                done = True
                reward = -1.
            else:
                done = False
                reward = 0.
        else:  # stick: play out the dealers hand, and score
            done = True
            while sum_hand(self.dealer) < 17:
                self.dealer.append(draw_card(self.np_random))
            reward = cmp(score(self.player), score(self.dealer))
            if self.natural and is_natural(self.player) and reward == 1.:
                reward = 1.5
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))

    def reset(self):
        self.dealer = draw_hand(self.np_random)
        self.player = draw_hand(self.np_random)
        return self._get_obs()
