"""
draw the concentric circles
"""
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from rattle_snake.constants import BeingCulture
from rattle_snake.draw import draw_pop_center, draw_support_node, draw_edge
from rattle_snake.node import Node, node_dist
from rattle_snake.cluster import (
    Cluster,
    find_closest_nodes,
    find_closest_nodes_between_clusters,
)
from rattle_snake.db_helpers import (
    db_setup,
    create_node,
    create_edge,
    create_connection,
    get_num_circles,
    get_plane_nodes,
    get_plane_edges,
    get_node_x_y,
)


def dist(x1, y1, x2, y2):
    return np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


class PlaneMap:
    """Class for holding the map a plane of existence.

    The higher the rank of the being, the closer to the
    center of the plane the being is allowed to traverse.

    Also the most resources exist in the center regions of
    the plane.
    """

    map_file_names = {
        BeingCulture.WEIRD: "images/weird_science_plane.png",
        BeingCulture.DEEP: "images/deep_denizen_plane.png",
        BeingCulture.DREAM: "images/dream_realm_plane.png",
    }
    colors = ["b", "g", "r", "cyan"]
    markers = ["*", ".", "p", "s", "v"]

    def __init__(
        self,
        db_file: str = "",
        being_culture: BeingCulture = BeingCulture.WEIRD,
        num_circles: int = 4,
    ):
        """Sets up the plane map

        Either creates all the nodes or loads them from an existing database

        Args:
            being_culture (str): One of "weird_science", "dream_realm", "deep_denizen"
            num_circles (int): Number of tiered circles to draw
            create_new_nodes (bool): Indicates whether to load existing or create new nodes.
            db_file (str): Path to a db_file
        """
        self.being_culture = being_culture
        if db_file:
            self.db_file = db_file
            db_setup(db_file=db_file)
            self.num_circles = get_num_circles(self.db_file, self.being_culture.value)
            self.load_map()
        else:
            db_file_name = self.generate_sqlite_db()
            self.db_file = db_file_name
            self.num_circles = num_circles
            db_setup(db_file=db_file_name)

            self.generate_map()

    def save(self):
        """Save an image of the map in is current state"""
        plt.savefig(self.title)

    def generate_sqlite_db(self) -> str:
        """Generate a new sqlite database"""

        now_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        db_file_name = f"nodes-{now_str}.db"

        return db_file_name

    def load_map(self) -> None:
        """Load the map data from the given db"""
        self.stratum_radii = 2.0
        self.stratum_boundaries = [
            ((i) * self.stratum_radii, (i + 1) * self.stratum_radii)
            for i in range(self.num_circles)
        ]

        # plotting setup
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect(1)
        self.title = self.map_file_names[self.being_culture]
        plt.title(self.title)

        self.draw_circles()

        self.nodes = get_plane_nodes(self.db_file, self.being_culture.value)

        for _, x, y, _, stratum_id, _, pop_center, _ in self.nodes:

            if pop_center:
                draw_pop_center(
                    self.ax,
                    x,
                    y,
                    self.colors[stratum_id - 1],
                    self.markers[stratum_id - 1],
                )
            else:
                draw_support_node(
                    self.ax,
                    x,
                    y,
                    self.colors[stratum_id - 1],
                    self.markers[stratum_id - 1],
                )

        self.edges = get_plane_edges(self.db_file, self.being_culture.value)

        for _, start, end, _, _ in self.edges:
            start_x, start_y = get_node_x_y(self.db_file, start)
            end_x, end_y = get_node_x_y(self.db_file, end)

            x_values = [start_x, end_x]
            y_values = [start_y, end_y]

            draw_edge(self.ax, x_values, y_values)

    def generate_map(self, k: int = 3, min_support: int = 3, max_support: int = 10):
        """Generate the map and nodes and edges to a database

        There are k population centers in each stratum.
        For each population center we generate a random nubmer of
        supporting/surround nodes.

        Each population center along with its supporting nodes
        forms a cluster which is enumerated by the node id
        of the population center. We random connect near by clusters
        """
        self.clusters = []
        self.nodes = []
        self.edges = []
        # nodes setup
        self.stratum_radii = 2.0
        self.stratum_boundaries = [
            ((i) * self.stratum_radii, (i + 1) * self.stratum_radii)
            for i in range(self.num_circles)
        ]

        # plotting setup
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect(1)
        self.title = self.map_file_names[self.being_culture]
        plt.title(self.title)

        self.draw_circles()

        # this delta keeps the generated nodes farther away from the boundary
        boundary_delta = 0.3

        stratum_num = 0
        # node id is the primary key of the nodes table
        node_id = 1
        edge_id = 1
        for color_num, bounds in enumerate(self.stratum_boundaries):
            print(f"stratum number {stratum_num}")
            stratum_num += 1

            # generate the pop centers
            for i in range(k):
                length = np.random.uniform(
                    bounds[0] + boundary_delta, bounds[1] - boundary_delta
                )
                print(f"length: {length}")
                angle = np.pi * np.random.uniform(0, 2)

                x = length * np.cos(angle)
                y = length * np.sin(angle)
                print(self.stratum_boundaries[i][0], self.stratum_boundaries[i][1])
                print(i, ":", x, y)

                draw_pop_center(self.ax, x, y, self.colors[color_num], self.markers[i])

                # insert population center into the table
                # is_population_center true == 1
                # yeild is fixed at 100 for now
                population_center_resource_yeild = np.random.randint(100, 200)
                # a population center's node_id is the same as it's cluster id
                node = (
                    node_id,
                    x,
                    y,
                    self.being_culture.value,
                    stratum_num,
                    node_id,
                    1,
                    population_center_resource_yeild,
                )
                pop_node = Node(
                    node_id=node_id,
                    x=x,
                    y=y,
                    plane=self.being_culture.value,
                    stratum_id=stratum_num,
                    cluster_id=node_id,
                    is_population_center=True,
                    resource_yeild=population_center_resource_yeild,
                )

                conn = create_connection(self.db_file)
                create_node(conn, node)
                pop_center_id = node_id
                pop_center_x = x
                pop_center_y = y
                node_id += 1
                self.nodes.append(node)

                # generate supporting nodes
                cluster_supporting_nodes = []
                num_support = np.random.randint(min_support, max_support + 1)
                for _ in range(num_support):
                    # controls how close the points are
                    delta = 0.1
                    l = np.random.uniform(length - delta, length + delta)
                    a = np.random.uniform(angle - np.pi / 8, angle + np.pi / 8)

                    x = l * np.cos(a)
                    y = l * np.sin(a)

                    draw_support_node(
                        self.ax, x, y, self.colors[color_num], self.markers[i]
                    )

                    yeild_delta = 50
                    supporting_node_resource_yeild = np.random.randint(
                        int(population_center_resource_yeild * 0.1),
                        int(population_center_resource_yeild * 0.6),
                    )
                    # 0 for not a population center
                    node = (
                        node_id,
                        x,
                        y,
                        self.being_culture.value,
                        stratum_num,
                        pop_center_id,
                        0,
                        supporting_node_resource_yeild,
                    )
                    supp_node = Node(
                        node_id=node_id,
                        x=x,
                        y=y,
                        plane=self.being_culture.value,
                        stratum_id=stratum_num,
                        cluster_id=pop_center_id,
                        is_population_center=False,
                        resource_yeild=supporting_node_resource_yeild,
                    )
                    cluster_supporting_nodes.append(supp_node)
                    create_node(conn, node)

                    # all supporting nodes are connected to their
                    # corresponding population center
                    x_values = [pop_center_x, x]
                    y_values = [pop_center_y, y]
                    draw_edge(self.ax, x_values, y_values)
                    # edge_id, start, end, length
                    edge = (
                        edge_id,
                        pop_center_id,
                        node_id,
                        self.being_culture.value,
                        node_dist(pop_node, supp_node),
                    )
                    create_edge(conn, edge)

                    edge_id += 1
                    node_id += 1
                    self.nodes.append(node)
                    self.edges.append(edge)

                self.clusters.append(
                    Cluster(
                        population_center=pop_node,
                        supporting_nodes=cluster_supporting_nodes,
                    )
                )

        cluster_connections = []

        # Each cluster is connected to it's closest neighbor
        # node by creating an edge between the two closest
        # supporting nodes (one from each cluster).
        for cluster in self.clusters:
            node1, node2, _ = find_closest_nodes(self.clusters, cluster)
            cluster_connections.append((node1.cluster_id, node2.cluster_id))
            edge = (
                edge_id,
                node1.node_id,
                node2.node_id,
                self.being_culture.value,
                node_dist(node1, node2),
            )
            conn = create_connection(self.db_file)
            create_edge(conn, edge)

            edge_id += 1

            x_values = [node1.x, node2.x]
            y_values = [node2.y, node2.y]
            draw_edge(self.ax, x_values, y_values)
            self.edges.append(edge)

        # setup a graph to detect disconnected components
        G = nx.Graph()
        for cluster_id_1, cluster_id_2 in cluster_connections:
            G.add_edge(cluster_id_1, cluster_id_2)

        cluster_dict = {c.cluster_id(): c for c in self.clusters}
        # if the clusters form a disconnected graph
        # keep adding edges until they are connected
        while not nx.is_connected(G):
            connected_components = nx.connected_components(G)
            comp1 = next(connected_components)
            comp2 = next(connected_components)
            comp_counter = 2

            cluster_group_1 = [cluster_dict[c] for c in comp1]
            cluster_group_2 = [cluster_dict[c] for c in comp2]

            node1, node2, min_dist = find_closest_nodes_between_clusters(
                cluster_group_1, cluster_group_2
            )

            for comp2 in connected_components:
                cluster_group_2 = [cluster_dict[c] for c in comp2]

                n1, n2, dist = find_closest_nodes_between_clusters(
                    cluster_group_1, cluster_group_2
                )

                if dist < min_dist:
                    node1 = n1
                    node2 = n2
                    min_dist = dist

                comp_counter += 1

            # update the graph
            G.add_edge(node1.cluster_id, node2.cluster_id)

            # create new edge
            edge = (
                edge_id,
                node1.node_id,
                node2.node_id,
                self.being_culture.value,
                node_dist(node1, node2),
            )
            conn = create_connection(self.db_file)
            create_edge(conn, edge)

            edge_id += 1

            x_values = [node1.x, node2.x]
            y_values = [node2.y, node2.y]
            draw_edge(self.ax, x_values, y_values)
            self.edges.append(edge)

            print(f"There are {comp_counter} connected Components")

    def draw_circles(self):
        """Draw the domain of the weird science beings"""
        angle = np.linspace(0, 2 * np.pi, 250)

        for i in range(self.num_circles):
            radius = (i + 1) * self.stratum_radii

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # draw a circle
            self.ax.plot(x, y, color="gray")


def main():
    plane_map = PlaneMap(being_culture=BeingCulture.WEIRD)
    plane_map.save()

    print("Drawing Complete.")
    print(f"saved to {plane_map.title}")

    # test the loading
    plane_map = PlaneMap(
        db_file=plane_map.db_file, being_culture=plane_map.being_culture
    )
    plane_map.save()
    print("Drawing complete from map loaded from the db")


if __name__ == "__main__":
    main()
