from importlib import import_module
import configparser
import argparse


def create_game(config):
    """Imports and instantiates an instenace of the game specified """
    game_module = config['game']['game module']
    game_class = config['game']['game class']
    cls = getattr(import_module(game_module), game_class)
    game_args = {'num_players': 4}
    return cls(**game_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get path to the game config.')
    parser.add_argument('--game_config',
                         help='Path to the ini file configuring the game to be played.')
    # parse arguements
    args = parser.parse_args()
    config_path = args.game_config

    # load config
    config = configparser.ConfigParser()
    config.read(config_path)

    # load game
    game = create_game(config)
    print(game.__dict__)
    print(f'Created {game.NAME}')

    game.play()

