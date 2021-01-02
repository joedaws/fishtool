from motherbrain.games.core.card_builder import CardBuilder
from motherbrain.games.core.deck_builder import DeckBuilder
import pytest


@pytest.fixture
def game_modules():
    return ['motherbrain.games.go_fish']

@pytest.fixture
def card_modules(game_modules):
    return {'motherbrain.games.go_fish': ['card']}


def test_card_builder(game_modules, card_modules):
    for game_module in game_modules:
        for card_module in card_modules[game_module]:
            cb = CardBuilder(game_module, card_module)
            fields = getattr(cb.card_info, 'CARD_FIELDS')
            print(fields)
            for field in fields:
                assert field[0] in cb.card_class.__annotations__
