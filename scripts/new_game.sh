#!/bin/bash

# IMPORTANT -- this script assumes that it is being run while cwd is the top level directory of the repository
#              that repo contain s motherbrain (the python module), data, scripts, and tests.
#
# IMPORTANT -- the argument of build $1 should be the snake case name of the game, e.g., for Go Fish,
#              name="go_fish".


templates_dir="scripts/templates"
policies_dir="motherbrain/brains/policies"
spaces_dir="motherbrain/brains/spaces"
game_module_dir="motherbrain/games"
players_dir="motherbrain/players"

build(){
  name="$1"
  echo "Creating empty directories and files for new game $name"
  policies "$name"
  spaces "$name" # create new spaces directory
  game_module "$name" # create new game module
  players "$name"
}

policies(){
  # function for creating the policy directory and files
  mkdir "$policies_dir/$1"
  touch "$policies_dir/$1/__init__.py"
  cat "$templates_dir/policies/random.txt" >> "$policies_dir/$1/random.py"
}

spaces(){
  # function for creating the spaces directory and files
  mkdir "$spaces_dir/$1"
  touch "$spaces_dir/$1/__init__.py"
  cat "$templates_dir/spaces/actions.txt" >> "$spaces_dir/$1/actions.py"
  cat "$templates_dir/spaces/observations.txt" >> "$spaces_dir/$1/observations.py"
}

game_module(){
  # create python modules and files
  mkdir "$game_module_dir/$1"  # main game module
  cat "$templates_dir/games/init.txt" >> "$game_module_dir/$1/__init__.py"
  cat "$templates_dir/games/game.txt" >> "$game_module_dir/$1/game.py"
  cat "$templates_dir/games/info.txt" >> "$game_module_dir/$1/info.py"
  cat "$templates_dir/games/state.txt" >> "$game_module_dir/$1/state.py"

  # create config directory and sample files
  mkdir "$game_module_dir/$1/config" # config directory
  cat "$templates_dir/games/config.txt" >> "$game_module_dir/$1/config/random.yaml" # random policy config
}

players(){
  cat "$templates_dir/players.txt" >> "$players_dir/$1.py"
}

"$@"
