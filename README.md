# Rattle Snake

Python library for generating random points

## Setup

### pyenv
https://github.com/pyenv/pyenv/

### Poetry
https://python-poetry.org/

## installing dependencies

``` shell
poetry install
```


## How to run
For now try

``` shell
poetry run python -m rattle_snake/plane_map.py
```

which should generate an image in the images directory for a certain
plane of existence.

## Exporting 

Not yet implemented

## desired features 

- want to be able formulate more urban versus not urban settings

- how should nodes be connected?

## How will this project communicate with the Beings simulation?

One pattern is to use files like csv or json.

Another is to consider using database, (start with SQLite why not).

Third option, translate this project to Elixir

# Streams

## October 26, 2022

- Whenever a new call to `generate_nodes` is called
  we'll put those nodes in a new database. Created
  a function to make a new database file and added the
  `create_new_nodes` argument of the constructor of
  `PlaneMap`.
- When instantiating a `PlaneMap` added the ability to load 
  from a database or create a database. When a database file 
  is passed to the constructor, the nodes are loaded from that
  database. On the other hand when there is no file passed 
  to the constructor, we create the nodes and a database
  where those nodes are stored.
  
## November 2, 2022

- Build connections between nodes
