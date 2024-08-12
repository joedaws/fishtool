# fishtool 

_fishtool_ is a project for exploring two things:

1. Building a simple cli to play a card game
2. Examining the strategies for games like go fish with weak reward signal

## Goals
- The game is implemented in such a way as to make it easy to capture _events_ that occur during game play.
- Having a uniform way to capture game events so that the RL algorithms implemented can be trained on any game which is implemented with the engine.

## Setup

Clone the repository and install the dependencies using
[poetry](https://python-poetry.org/docs/):

``` bash
poetry install
```

Below are scripts run using =poetry='s =run= command.  

## Testing

``` bash
poetry run test
```

## Playing Go Fish on the command line

### Play a game
To run a game of GoFish between you and 3 computer players with purely random policies use:

``` bash
poetry run play
```


### Automatic play with random policy
To run a game of GoFish between four players all using random policies use:

```
poetry run play_random
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
