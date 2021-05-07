from importlib import import_module
import yaml
from yaml import Loader
import argparse


def create_game(config, record):
    """Imports and instantiates an instenace of the game specified """
    # import game class
    game_module = config['game']['game module']
    game_class = config['game']['game class']
    cls = getattr(import_module(game_module), game_class)
    policies = create_policies(config)
    # import and create policy types
    return cls(policies, record)


def create_policies(config):
    """Import and create policy classes for players."""
    # get player's names
    player_names = config['players']['names']
    # get policy types
    player_policy_modules = [config[name]['policy module']
                             for name in player_names]
    # get policy class name
    player_policy_classes = [config[name]['policy class']
                             for name in player_names]
    # import policies into list
    policy_list = [getattr(import_module(policy_module), policy_class)
                   for policy_module, policy_class in
                   zip(player_policy_modules, player_policy_classes)]
    return policy_list


def main():
    """Parse configs, create game, and play."""
    parser = argparse.ArgumentParser(description='Get path to the game config.')
    parser.add_argument('--game-config',
                        help='Path to the yaml file configuring the game to be played.')
    parser.add_argument('--record',
                        type=bool,
                        default=False,
                        help='flag to indicate whether the game state data should be saved.')

    # parse arguments
    args = parser.parse_args()
    config_path = args.game_config
    record = args.record

    # load config
    with open(config_path, 'rb') as stream:
        config = yaml.load(stream, Loader=Loader)

    # load game
    game = create_game(config, record)
    print(f'Created {game.NAME}')

    game.play()

if __name__ == "__main__":
    main()
