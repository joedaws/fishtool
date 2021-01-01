from dataclasses import dataclass
from aicard.players.base import Player


@dataclass
class SuccessEvent:
    """Records when a player was successful in an action."""
    player: Player


@dataclass
class FailEvent:
    """Records when a player has failed to do something."""
    player: Player


@dataclass
class DrawEvent:
    """Stored data from a draw."""
    player: Player
    number: int = 1


@dataclass
class AskEvent:
    """Stores data of an ask."""
    player: Player
    opponent: Player
    rank: str

@dataclass
class ExchangeEvent:
    """Stores data for an exchange.

    Fields:
        source (Player): Giving players index.
        destination (Player): Receiving players index.
        rank (str): Ranks of card(s) being exchanged.
        number (int): Number of cards with specific rank being exchanged.
    """
    source: Player
    destination: Player
    rank: str
    number: int


@dataclass
class BookEvent:
    """Event for when a players makes a book."""
    player: Player
    rank: str
    number: int = 4


@dataclass
class RemovePlayerEvent:
    """Event for when a player is removed from the game."""
    player_to_remove: Player
