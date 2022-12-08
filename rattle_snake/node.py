from dataclasses import dataclass
import numpy as np


@dataclass
class Node:
    node_id: int
    x: float
    y: float
    plane: str
    stratum_id: int
    cluster_id: int
    is_population_center: bool
    resource_yeild: int


def node_dist(n1: Node, n2: Node) -> float:
    """Find the distance between nodes."""
    x1 = n1.x
    y1 = n1.y
    x2 = n2.x
    y2 = n2.y

    return np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def tuple_to_node(
    node_id, x, y, plane, stratum_id, cluster_id, is_population_center, resource_yeild
):
    return Node(
        node_id=node_id,
        x=x,
        y=y,
        plane=plane,
        stratum_id=stratum_id,
        cluster_id=cluster_id,
        is_population_center=is_population_center,
        resource_yeild=resource_yeild,
    )
