# Rattle Snake

Python library for generating random points


![Plane Map of Weird Science](images/weird_science_plane.png)

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

## How are nodes generated?

There are multiple planes of existence, one for each of the 3
cultures of beings from the [beings](https://github.com/joedaws/beings) simulation.
Each plane is made up of concentric circles corresponding to the different ranks
that beings might have. For each circle, there are two kinds of categories of nodes,
population centers and supporting nodes. 

The population centers are connected to all of the their supporting nodes, and 
some of the supporting nodes are connected to the supporting nodes of other 
population centers.


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
