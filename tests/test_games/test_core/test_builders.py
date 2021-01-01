from aicard.games.core.card_builder import CardBuilder
from aicard.games.core.deck_builder import DeckBuilder
import pytest


@pytest.fixture
def game_modules():
    return ['aicard.games.go_fish']


def test_card_builder(game_modules):
    for module in game_modules:
        cb = CardBuilder(module)
        fields = getattr(cb.game_info, 'CARD_FIELDS')
        print(fields)
        for field in fields:
            assert field[0] in cb.card_class.__annotations__
