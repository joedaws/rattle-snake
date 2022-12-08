"""
Run this script to seed the database
"""
import click

from rattle_snake.db_helpers import generate_sqlite_db_file, db_setup
from rattle_snake.plane_map import PlaneMap
from rattle_snake.constants import BeingCulture


def seed_nodes_and_edges(db_file: str):
    """Creates entries in the database for all nodes and edges for each of the three planes"""
    plane_map = PlaneMap(being_culture=BeingCulture.WEIRD)
    plane_map.save_to_db(db_file=db_file)
    plane_map = PlaneMap(being_culture=BeingCulture.DEEP)
    plane_map.save_to_db(db_file=db_file)
    plane_map = PlaneMap(being_culture=BeingCulture.DREAM)
    plane_map.save_to_db(db_file=db_file)


def seed_db(db_file: str = "hello.db"):
    """This seeds the database file"""
    db_setup(db_file=db_file)
    click.echo(f"setup db_file {db_file}")
    seed_nodes_and_edges(db_file)


if __name__ == "__main__":
    seed_db()
