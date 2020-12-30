from importlib import import_module 
import configparser
import argparse


def create_game(config):
    """Imports and instantiates an instenace of the game specified """
    # import game class
    game_module = config['game']['game module']
    game_class = config['game']['game class']
    cls = getattr(import_module(game_module), game_class)
    policies = create_policies(config)
    # import and create policy types
    return cls(policies)


def create_policies(config):
    """Import and create policy classes for players."""
    # get player's names
    player_names = config['players']['names'].split(',')
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
                        help='Path to the ini file configuring the game to be played.')
    # parse arguments
    args = parser.parse_args()
    config_path = args.game_config

    # load config
    config = configparser.ConfigParser()
    config.read(config_path)

    # load game
    game = create_game(config)
    print(f'Created {game.NAME}')

    game.play()

if __name__ == "__main__":
    main()
