from dataclasses import dataclass


@dataclass
class DrawEvent:
    """Stored data from a draw."""
    player: int
    number: int = 1


@dataclass
class AskEvent:
    """Stores data of an ask."""
    player: int
    rank: str


@dataclass
class ExchangeEvent:
    """Stores data for an exchange.

    Attributes:
        player_giving (int): Giving players index.
        player_receiving (int): Receiving players index.
        rank (str): Ranks of card(s) being exchanged.
        number (int): Number of cards with specific rank being exchanged.
    """
    player_giving: int
    player_receiving: int
    rank: str
    number: int


@dataclass
class BookEvent:
    """Event for when a players makes a book."""
    player: int
    rank: str
    number: int = 4
