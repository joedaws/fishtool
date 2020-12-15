from dataclasses import dataclass


@dataclass
class ExchangeEvent:
    """Stores data for an exchange.
    
    Attributes:
        player_giving (int): Giving player index.
        player_receiving (int): Receiving player index.
        rank (str): Ranks of card(s) being exchanged.
        number (int): Number of cards with specific rank being exchanged.
    """
    player_giving: int
    player_receiving: int
    rank: str
    number: int

@dataclass
class BookEvent:
    """Event for when a player makes a book."""
    player: int
    rank: str
    number: int = 4
