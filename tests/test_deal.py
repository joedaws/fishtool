from card_player.deck.deck import Deck
from card_player.player.player import GoFishPlayer

# make some players
p1 = GoFishPlayer('player1')
p2 = GoFishPlayer('player2')

# list of players for dealing
players = [p1, p2]

# make a deck
deck = Deck()
deck.shuffle()

# deal some cards
HAND_SIZE = 20 
for _ in range(HAND_SIZE):
    for p in players:
        p.draw(deck)

# print hands for verification later
for p in players:
    print(p.name, len(p.hand))
    for c in p.hand:
        print(c)
    print('\n')

# player1 asks for a card from player2
ask_rank = p1.hand[0].rank
print(f"p1 is asking for a {ask_rank}")
p1.ask(p2,ask_rank)

# print hands to see if cards were exchanged
for p in players:
    print(p.name, len(p.hand))
    for c in p.hand:
        print(c)
    print('\n')


