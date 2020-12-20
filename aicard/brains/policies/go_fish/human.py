import sys
from aicard.brains.spaces.go_fish.actions import Actions
from aicard.engine.io.getch import getch


class GoFishHumanPolicy:
    """Human input policy for Go Fish.

    When this policy is used, the user is asked
    to for input to choose actions.

    The rank_to_seek and player_to_ask method list numbered
    choices and the user inputs one charater to choose one
    of the available options.
    """
    def __init__(self):
        self._actions = None

    @property
    def actions(self):
        """An instance of the Actions class"""
        return self._actions

    @actions.setter
    def actions(self, new_actions: Actions):
        """Overwrite the actions stored in Actions."""
        self._actions = new_actions

    def rank_to_seek(self):
        """Ask user to choose one of the available ranks."""
        ranks = self.actions.valid_ranks
        # prompt user for character.
        rank_options = ["".join([rank, ':', str(i), '\n'])
                        for i, rank in enumerate(ranks)]
        print("".join(['Your ranks:\n']+rank_options))
        sys.stdout.write("Choose a rank: ")
        sys.stdout.flush()
        # query user for input
        ask_idx = getch()
        sys.stdout.write(ask_idx+'\n\n')
        sys.stdout.flush()
        return ranks[int(ask_idx)]

    def player_to_ask(self):
        """Ask user to choose one of the available opponents."""
        opponents = self.actions.valid_opponents
        # prompt user to choose an opponent.
        opponent_options = ["".join([opp.name, ' : ', str(i), '\n'])
                            for i, opp in enumerate(opponents)]
        print("".join(['Your opponents:\n']+opponent_options))
        sys.stdout.write("Choose an opponent: ")
        sys.stdout.flush()
        # query user for input
        ask_idx = getch()
        sys.stdout.write(ask_idx+'\n\n')
        sys.stdout.flush()
        return opponents[int(ask_idx)]

    def sample(self):
        """Return the required choices."""
        return self.player_to_ask(), self.rank_to_seek()
