import yaml
from cartomancy.games.run import create_game
from yaml import Loader


def human():
    """Parse configs, create game, and play."""
    go_fish_config_path = 'config/go_fish/one_human.yaml'

    # load config
    with open(go_fish_config_path, 'rb') as stream:
        config = yaml.load(stream, Loader=Loader)

    # load game
    game = create_game(config)

    game.play()


def random():
    """Parse configs, create game, and play."""
    go_fish_config_path = 'config/go_fish/random.yaml'

    # load config
    with open(go_fish_config_path, 'rb') as stream:
        config = yaml.load(stream, Loader=Loader)

    # load game
    game = create_game(config)

    game.play()
