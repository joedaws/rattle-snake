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
