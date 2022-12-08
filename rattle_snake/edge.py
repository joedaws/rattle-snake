from dataclasses import dataclass


@dataclass
class Edge:
    edge_id: int
    start_node_id: int
    end_node_id: int
    plane: str
    length: float


def tuple_to_edge(edge_id, start_node_id, end_node_id, plane, length):
    return Edge(
        edge_id=edge_id,
        start_node_id=start_node_id,
        end_node_id=end_node_id,
        plane=plane,
        length=length,
    )
