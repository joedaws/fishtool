import gym
from gym import spaces
from gym.utils import seeding


class GoFishEnv(gym.Env):
    """Go Fish environments implementation.

    Action Space:
        Each players may ask for one of the ranks from one of the players.
        Therefore, the action spaces is a tuple with the number of players
        and a discrete spaces of 13 (the total number of ranks).

    Observation Space:
        Each players

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
