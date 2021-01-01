import sys
from motherbrain.brains.spaces.go_fish.actions import Actions
from motherbrain.engine.io.getch import getch


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
        # get user input
        user_input = self.ask_user_for_rank()

        # create valid choice mapping
        user_input_to_idx = {str(i+1): i for i in range(len(self.actions.valid_ranks))}
        user_input_to_idx['q'] = 14

        # process user input
        try:
            ask_idx = user_input_to_idx[user_input]
            if ask_idx == 14:
                # quit the game
                sys.exit('quitting the game!')
            else:
                ask_rank = self.actions.valid_ranks[ask_idx]
        except KeyError:
            # ask for another rank
            print(f'The choice {user_input} is invalid. Please choose another.')
            ask_rank = self.rank_to_seek()

        return ask_rank

    def player_to_ask(self):
        """Ask user to choose one of the available opponents."""
        # get user input
        user_input = self.ask_user_for_opp()

        # create valid choice mapping
        user_input_to_idx = {str(i+1): i for i in range(len(self.actions.valid_opponents))}
        user_input_to_idx['q'] = 14

        # process user input
        try:
            ask_idx = user_input_to_idx[user_input]
            if ask_idx == 14:
                # quit the game
                sys.exit('quitting the game!')
            else:
                ask_opp = self.actions.valid_opponents[ask_idx]
        except KeyError:
            # ask for another opponent
            print(f'The choice {user_input} is invalid. Please choose another.')
            ask_opp = self.player_to_ask()

        return ask_opp

    def sample(self):
        """Return the required choices."""
        return self.player_to_ask(), self.rank_to_seek()

    def ask_user_for_rank(self):
        """Ask user to choose a rank."""
        ranks = self.actions.valid_ranks
        # prompt user for character.
        rank_options = ["".join(['option ', str(i+1), ' : ', rank, '\n'])
                        for i, rank in enumerate(ranks)]
        print("".join(['Your ranks:\n']+rank_options))
        sys.stdout.write("Choose a rank: ")
        sys.stdout.flush()
        # query user for input
        ask_idx_plus_one = getch()
        sys.stdout.write('option ' + ask_idx_plus_one + '\n\n')
        sys.stdout.flush()

        return ask_idx_plus_one 

    def ask_user_for_opp(self):
        """Ask user to choose an opponent."""
        opponents = self.actions.valid_opponents
        # prompt user to choose an opponent.
        opponent_options = ["".join(['option ', str(i+1), ' : ', opp.name, '\n'])
                            for i, opp in enumerate(opponents)]
        print("".join(['Your opponents:\n']+opponent_options))
        sys.stdout.write("Choose an opponent: ")
        sys.stdout.flush()
        # query user for input
        ask_idx_plus_one = getch()
        sys.stdout.write('option ' + ask_idx_plus_one + '\n\n')
        sys.stdout.flush()

        return ask_idx_plus_one

    @staticmethod
    def process_user_input(char):
        """Check to see if the user would like to quit.

        Also checks for 0 char, in which case the index is -1
        or the last element of the choices. In this case, we will 
        set the char to 14 which will never be a valid index. This
        will cause an index error later which will be captured
        in rank_to_ask or player_to_seek
        """
        if char != 'q':
            idx = int(char) - 1
        elif char == '0':
            idx = 14
        else:
            idx = char

        return idx
