import sqlite3

from rattle_snake.constants import PLANES_DB_FILE


CREATE_NODES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS nodes (
  node_id INTEGER PRIMARY KEY,
  x REAL NOT NULL,
  y REAL NOT NULL,
  stratum_id INTEGER NOT NULL,
  is_population_center INTERGER NOT NULL,
  resource_yeild INTEGER NOT NULL
);
"""

INSERT_NODE_QUERY = """
INSERT INTO nodes (x,y,stratum_id,is_population_center,resource_yeild)
VALUES(?,?,?,?,?)
"""


def create_connection(db_file=PLANES_DB_FILE):
    """returns a connection to the db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def create_nodes_table(conn):
    """Create the Nodes table if it doesn't yet exist."""
    cur = conn.cursor()
    cur.execute(CREATE_NODES_TABLE_QUERY)
    conn.commit()


def create_node(conn, node):
    """
    node is a list/tuple of 5 values
    - x
    - y
    - stratum_id
    - is_population_center
    - resource_yeild
    """
    cur = conn.cursor()
    cur.execute(INSERT_NODE_QUERY, node)
    conn.commit()
    print(f"added node {node}")


def db_setup():
    """Sets up the database with tables if it hasn't already been setup."""
    conn = create_connection()
    create_nodes_table(conn)
