import sqlite3

from rattle_snake.constants import PLANES_DB_FILE


CREATE_NODES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS nodes (
  node_id INTEGER PRIMARY KEY,
  x REAL NOT NULL,
  y REAL NOT NULL,
  plane TEXT NOT NULL,
  stratum_id INTEGER NOT NULL,
  cluster_id INTEGER NOT NULL,
  is_population_center INTERGER NOT NULL,
  resource_yeild INTEGER NOT NULL
);
"""

# start and end are the node_id fields of the
# starting and ending node of the edge
CREATE_EDGES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS edges (
  edge_id INTEGER PRIMARY KEY,
  start INTEGER NOT NULL,
  end INTEGER NOT NULL,
  plane TEXT NOT NULL,
  length INTEGER NOT NULL
);
"""


INSERT_NODE_QUERY = """
INSERT INTO nodes (node_id,x,y,plane,stratum_id,cluster_id,is_population_center,resource_yeild)
VALUES(?,?,?,?,?,?,?,?)
"""


INSERT_EDGE_QUERY = """
INSERT INTO edges (edge_id,start,end,plane,length)
VALUES(?,?,?,?,?)
"""

NUM_CIRCLES_QUERY = """
SELECT MAX(stratum_id) from nodes where plane = ?;
"""


GET_PLANE_NODES_QUERY = """
SELECT * from nodes where plane = ?;
"""


GET_PLANE_EDGES_QUERY = """
SELECT * from edges where plane = ?;
"""

GET_NODE_X_Y_QUERY = """
SELECT x, y from nodes where node_id = ?;
"""


def create_connection(db_file):
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


def create_edges_table(conn):
    """Create the Edges table if it doesn't yet exist."""
    cur = conn.cursor()
    cur.execute(CREATE_EDGES_TABLE_QUERY)
    conn.commit()


def create_node(conn, node):
    """
    node is a list/tuple of 6 values
    - id
    - x
    - y
    - plane
    - stratum_id
    - cluster_id
    - is_population_center
    - resource_yeild
    """
    cur = conn.cursor()
    cur.execute(INSERT_NODE_QUERY, node)
    conn.commit()
    print(f"added node {node}")


def create_edge(conn, edge):
    """
    edge is a tuple of 4 values
    - edge_id
    - start
    - end
    - plane
    - length

    The start and end are node_ids of the nodes
    which the edge connects.
    """
    cur = conn.cursor()
    cur.execute(INSERT_EDGE_QUERY, edge)
    conn.commit()
    print(f"added edge {edge}")


def db_setup(db_file: str):
    """Sets up the database with tables if it hasn't already been setup."""
    conn = create_connection(db_file=db_file)
    create_nodes_table(conn)
    create_edges_table(conn)


def get_num_circles(db_file: str, plane: str) -> int:
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(NUM_CIRCLES_QUERY, (plane,))
    rows = cur.fetchall()
    num_circles = int(rows[0][0])
    print(f"The number of cirlces retrived for {plane} was {num_circles}")
    return num_circles


def get_plane_nodes(db_file: str, plane: str):
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(GET_PLANE_NODES_QUERY, (plane,))
    rows = cur.fetchall()
    return rows


def get_plane_edges(db_file: str, plane: str):
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(GET_PLANE_EDGES_QUERY, (plane,))
    rows = cur.fetchall()
    return rows


def get_node_x_y(db_file: str, node_id: int):
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(GET_NODE_X_Y_QUERY, (node_id,))
    rows = cur.fetchall()
    # should only ever return info on ONE node
    return rows[0]
