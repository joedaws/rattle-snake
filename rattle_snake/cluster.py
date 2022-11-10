from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from sklearn.neighbors import NearestNeighbors


from rattle_snake.node import Node


@dataclass
class Cluster:
    population_center: Node
    supporting_nodes: List[Node]

    def cluster_id(self) -> int:
        return self.population_center.node_id


def find_closest_nodes(clusters: List[Cluster], cluster: Cluster) -> Tuple[Node, Node]:
    """Find the nearest node among all other cluster's nodes to one of the cluter nodes"""

    cluster_nodes = [node for node in cluster.supporting_nodes]
    cluster_nodes.append(cluster.population_center)
    number_of_nodes_in_cluster = len(cluster_nodes)
    neigh = NearestNeighbors(n_neighbors=number_of_nodes_in_cluster)
    # the population center also needs to be included
    points = [(node.x, node.y) for node in cluster_nodes]
    neigh.fit(points)

    other_cluster_supporting_nodes = []
    for other_cluster in [c for c in clusters if c.cluster_id != cluster.cluster_id]:
        for node in other_cluster.supporting_nodes:
            other_cluster_supporting_nodes.append(node)

    node2 = other_cluster_supporting_nodes[0]
    distances, indexes = neigh.kneighbors([(node2.x, node2.y)])
    node1 = cluster_nodes[indexes[0][0]]
    min_distance = distances[0][0]
    for n2 in other_cluster_supporting_nodes[1:]:
        distances, indexes = neigh.kneighbors([(n2.x, n2.y)])
        distance = distances[0][0]
        if distance < min_distance:
            node1 = cluster_nodes[indexes[0][0]]
            node2 = n2
            min_distance = distance

    return node1, node2
