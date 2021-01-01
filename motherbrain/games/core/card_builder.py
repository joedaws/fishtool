from importlib import import_module
from dataclasses import make_dataclass


class CardBuilder:
    """Class for building card classes.

    Examples:
        For a standard playing card, we can make the
        card_fields = [('rank', str), ('suit', str)]
    """
    def __init__(self, game_module):
        self.game_info = import_module(game_module)
        name = getattr(self.game_info, 'NAME')
        fields = getattr(self.game_info, 'CARD_FIELDS')
        str_fun = getattr(self.game_info, 'CARD_STR_FUN')
        self.card_class = self.make_card_class(name, fields, str_fun)

    @staticmethod
    def make_card_class(name, fields, str_fun):
        """make a dataclass with the desired fields."""
        card_cls = make_dataclass(name+'Card',
                                  fields,
                                  namespace={'__str__': str_fun})

        return card_cls

    def build_card(self, fields):
        """Build an instance of the card with the provided fields."""
        card = self.card_class(**fields)
        return card
