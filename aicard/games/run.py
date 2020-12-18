from importlib import import_module
import configparser
import argparse


def create_game(config):
    game_module = config['game']['game module']
    game_class = config['game']['game class']
    cls = getattr(import_module(game_module), game_class)
    game_args = {'num_players':4}
    print(cls)
    game = cls(**game_args)
    return game

def main():
    # make some players
    p1 = GoFishPlayer('player1')
    p2 = GoFishPlayer('player2')

    # list of players for dealing
    players = [p1, p2]

    # make a deck
    deck = Deck()

    # deal cards to players
    deal(deck, p1, p2)

    for i in range(NUM_TURNS):
        print(f"\n\nTurn {i}:")
        play_turn(deck, p1, p2)
        play_turn(deck, p2, p1)
        print(f"{p1.name} has {len(p1.hand)} cards and {len(p1.books)} books")
        #print(hand_str(p1))
        print(f"{p2.name} has {len(p2.hand)} cards and {len(p2.books)} books.")
        #print(hand_str(p2))
        print(f"The deck has {len(deck.cards)} cards remaining.")

        if len(p1.books) + len(p2.books) == 13:
            if len(p1.books) > len(p2.books):
                print(f"The game is over, {p1.name} wins!")
            elif len(p2.books) > len(p1.books):
                print(f"The game is over, {p2.name} wins!")
            break


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

