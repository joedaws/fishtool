import sys
from random import randint
from aicard.deck import Deck
from aicard.player import GoFishPlayer
from aicard.policy import GoFishRandomPolicy


HAND_SIZE = 7
NUM_TURNS = 30


def show_state(player):
    """Returns string representation of a players state"""
    state_str = f"{player.name} state:\n"
    for rank in player.state:
        if player.state[rank]:
            state_str += rank + ": "
        for suit in player.state[rank]:
            state_str += suit + " "
        if player.state[rank]:
            state_str += "\n"

    return state_str


def deal(deck, p1, p2):
    """Deal cards from deck to p1 and p2"""
    deck.shuffle()

    # deal some cards
    for _ in range(HAND_SIZE):
        p1.draw(deck)
        p2.draw(deck)

    # show the state of each player's hand
    print(show_state(p1))
    print(show_state(p2))


def play_turn(deck, player, opponent):
    """Player asks opponent for a card and goes fish if no exchange."""
    if len(player.hand) == 0:
        if len(deck.cards) > 0:
            player.draw(deck)

    keep_asking = len(player.hand) > 0
    """
    if len(player.hand) > 0:
        keep_asking = True
    else:
        keep_asking = False
    """

    asks = 0
    while keep_asking:
        # use policy to choose action
        ask_rank = GoFishRandomPolicy(player.hand).rank_to_seek()

        #rand_idx = randint(0, len(player.hand)-1)
        #ask_rank = player.hand[rand_idx].rank
        print(f"{player.name} is asking for a {ask_rank}")
        keep_asking = player.ask(opponent, ask_rank)
        asks += 1
        if keep_asking:
            print(f"{player.name} obtained at least one {ask_rank} from {opponent.name}.")
        else:
            print(f"{player.name} did not obtain a {ask_rank} from {opponent.name}.")

        if len(player.hand) == 0:
            if len(deck.cards) > 0:
                player.draw(deck)
            else:
                keep_asking = False

    if len(deck.cards) == 0:
        print(f"The Deck is empty.")
    elif asks == 1:
        print(f"{player.name} is drawing a card.")
        player.draw(deck)


def hand_str(player):
    """Returns single line string representation of hand"""
    hand_str = ""

    for c in player.hand:
        hand_str += str(c) + " "

    return hand_str


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
    main()
