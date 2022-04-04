# Games

Different games are implemented in this submodule. It also contains the submodule __core__ where
some common tools for different kinds of games are implemented.

#### Core
This module contains common objects useful for building card games such as Card and Deck objects. It also
defines some Event classes which describe the change in state of the game.

---
---

# Go Fish
The rules of __Go Fish__ can be found on [Bicycle's website](https://bicyclecards.com/how-to-play/go-fish/). 

---
---

# Magnum Opus
Magnum Opus is a multi-deck card game which is intended to be played by 16 to 64 players.
The objective of the game is to have the most points when the game is over.

### The philosopher's stone
This might be added, but not sure yet. . .

Creating a philosopher's stone is the primary objective of 
each alchemist. Once an alchemist transmutes materials into a 
philosopher's stone, that alchemist leaves the game. 

### Setup

Each player begins the game with one level 1 alchemist and
5 materials cards drawn at random from the materials deck.

---

### Phases of play

#### Opening Phase

#### Transmutation Phase

During the __transmutation phase__ of each player's turn, each
alchemist controlled by the player may transmute one material 
from the players hand or transmute a material in taccording to their skill level a

---

###The Decks

Two decks are used to play Magnum Opus, an alchemist deck filled with cards representing different 
alchemists and a Metallurgy deck which is composed of cards representing different
metals and alchemical processes which may be applied to them.

#### Card Properties
| Card Type  | Properties |
| :---: | :---: |
| Alchemist  | Name, Zodiac Sign, Element |
| Material   | Metal Type, Planet |
| Process | Process Type | 

#### Zodiac sign and elements

| Zodiac Sign | Element |
| :---: | :---: |
|Aries | Fire |
|Taurus| Earth |
|Gemini| Air |
|Cancer| Water |
|Leo | Fire |
|Virgo| Earth |
|Libra | Air |
|Scorpio | Water |
|Sagittarius| Fire |
|Capricorn | Earth |
|Aquarius| Air |
|Pisces| Water |

#### Materials Cards

| Planet | Metal | Rank |
| :---: | :---: | :---: |
| Sun | Gold | S |
| Moon | Silver | A |
| Mercury | Quicksilver | A |
| Venus | Copper | B |
| Mars | Iron | B |
| Jupiter | Tin | B |
| Saturn | Lead | C |

#### Transmutation skill level

An alchemist can use transmutation to turn lower rank
metals into higher rank metals. Depending on their skill, they
may improve the rank of material by one, two, or three. 
That is, an alchemist will transmutation skill level 1 alchemist 
can improve any material by one rank, e.g., turn lead 
which is a C rank material into any of the B level materials. 
A skill level 2 alchemist can improve the material two 
ranks, and a skill level 3 alchemist can improve any rank material 
into gold.

#### Object of the Game

The goal is to be the last player remaining after all other players
have been eliminated.

#### Elimination

