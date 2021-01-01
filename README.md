# motherbrain

__Status__: pre-alpha

_motherbrain_ is a project to explore how to use machine learning to create 
game playing agents which are fun to play against. This python module implements 
both games and machine learning tools. The games are implemented in such a way
as to make it easy to capture _events_ that occur during game play. These events
can later be used to train agents to play the game.

Currently, only _go fish_ is implemented. This project is structed in such 
a way as to allow for construction of new games for which agents may 
be trained to pay.

## Description

This project is under development.

## Getting Started

### Dependencies

* python 3.7.x or greater.

### Installing

* Clone this repository.  
* In the future tox support will be added.

### Card Games 

#### Go fish
* Currently, only go fish is implemented. 
* To run a game of GoFish between four players all using random policies use:

```
python -m aicard.game.run --game_config=aicard.games.go_fish.config.random.yaml
```

## Version History

This project is still under development.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
