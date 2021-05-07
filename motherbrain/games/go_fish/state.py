from __future__ import annotations
from dataclasses import dataclass
from motherbrain.brains.spaces.go_fish.observations import Observations
from motherbrain.games.core.deck import Deck
from motherbrain.games.core.deck_builder import DeckBuilder
from motherbrain.games.core.game import GameState
from motherbrain.games.core.game import GameStateObserver
from motherbrain.players.go_fish import GoFishPlayer
from time import gmtime, strftime


@dataclass
class GoFishStateStep:
    """A class for storing the state of a go fish game at a particular step."""
    players: list
    player_states: dict 
    deck: Deck
    observations: dict


class GoFishStateObserver(GameStateObserver):
    """
    Observer of the go fish game. Records events after being notified by the GoFishState.
    """
    def __init__(self, record):
        self.record = record
        self._history = []
        self.id = strftime("%a-%d-%b-%Y-%H-%M-%S", gmtime())

    def update(self, game_state: GoFishState):
        """
        recieve updates from the game state and
        append to the record.

        For reinforcement learning we will need 
        - player state for each player
        - The deck 
        - The observations made by each player

        Policy probabilities or state will be recorded by a policy observer
        """
        step_data = {
            'players': game_state.players,
            'player_states': {player: player.state for player in game_state.players},
            'deck': game_state.deck,
            'observations': game_state.observations
        }

        step = GoFishStateStep(**step_data)
        if self.record:
            self.append(step)

    def append(self, step: GoFishStateStep) -> None:
        """Record events in the step to this history, an instance of the step data."""
        self._history.append(step)

    def record_history(self):
        """Record a history of states"""
        if self.record:
            self.write_to_library('go_fish', self._history)


class GoFishState(GameState):
    """A class representing the state of the go fish game."""

    get_deck = DeckBuilder('motherbrain.games.go_fish', 'card').build_deck

    def __init__(self, num_players=4):
        player_names = ['player ' + str(i) for i in range(num_players)]
        self.players = {GoFishPlayer(name): i for i, name in enumerate(player_names)}
        self._set_player_indices()
        self.opponents_map = self._setup_opponents_map()

        self.deck = self.get_deck()

        self.observations = {player: Observations(player, self.opponents_map[player])
                             for player in self.players}

        self._observers = []

    def reset(self):
        """Reset to an initial state."""
        self.deck = self.get_deck()
        self.observations = {player: Observations(player, self.opponents_map[player])
                             for player in self.players}

    def hands(self):
        """Returns hands of all players.

        Returns:
            dictionary whose keys are players and whose values are the corresponding player's hand.
        """
        return {player: player.hand for player in self.players}

    def update(self, event):
        """update the state according to the event."""

        # update observations
        for player in self.players:
            self.observations[player].update(event)

        # need to notify recorder so that it can make a
        # record of the state
        self.notify()

    def attach(self, observer: GoFishStateObserver) -> None:
        """Attach a game state observer."""
        self._observers.append(observer)

    def detach(self, observer: GoFishStateObserver) -> None:
        """Attach a go fish state observer"""
        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify State Observers of change to state."""
        for observer in self._observers:
            observer.update(self)

    def _set_player_indices(self):
        """Set the index attribute of the players."""
        for player, index in self.players.items():
            player.index = index

    def _setup_opponents_map(self):
        """Create a dictionary describing the opponents of each players."""
        indices = list(self.players.values())
        return {player: [opponent for opponent in self.players if opponent != player] for player in self.players}


