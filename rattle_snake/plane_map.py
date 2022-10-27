"""
draw the concentric circles
"""
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from rattle_snake.constants import BeingCulture
from rattle_snake.db_helpers import (
    db_setup,
    create_node,
    create_connection,
    get_num_circles,
    get_plane_nodes,
)


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
            self.load_nodes()
        else:
            db_file_name = self.generate_sqlite_db()
            self.db_file = db_file_name
            self.num_circles = num_circles
            db_setup(db_file=db_file_name)

            self.generate_nodes()

    def save(self):
        """Save an image of the map in is current state"""
        plt.savefig(self.title)

    def generate_sqlite_db(self) -> str:
        """Generate a new sqlite database"""

        now_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        db_file_name = f"nodes-{now_str}.db"

        return db_file_name

    def load_nodes(self) -> None:
        """Load the nodes for the given plane from the given db"""
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

        for _, x, y, _, stratum_id, _, _ in self.nodes:

            self.ax.scatter(
                x,
                y,
                color=self.colors[stratum_id - 1],
                marker=self.markers[stratum_id - 1],
                linewidths=3.0,
            )

    def generate_nodes(self, k: int = 3, min_support: int = 3, max_support: int = 10):
        """Generate the nodes.

        There are k population centers in each stratum.
        For each population center we generate a random nubmer of
        supporting/surround nodes.

        Sets up the nodes property of this class
        """
        self.nodes = []
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

        stratum_num = 0
        for color_num, bounds in enumerate(self.stratum_boundaries):
            print(f"stratum number {stratum_num}")
            stratum_num += 1

            # generate the pop centers
            for i in range(k):
                length = np.random.uniform(bounds[0], bounds[1])
                print(f"length: {length}")
                angle = np.pi * np.random.uniform(0, 2)

                x = length * np.cos(angle)
                y = length * np.sin(angle)
                print(self.stratum_boundaries[i][0], self.stratum_boundaries[i][1])
                print(i, ":", x, y)

                self.ax.scatter(
                    x,
                    y,
                    color=self.colors[color_num],
                    marker=self.markers[i],
                    linewidths=3.0,
                )

                # insert population center into the table
                # is_population_center true == 1
                # yeild is fixed at 100 for now
                population_center_resource_yeild = np.random.randint(100, 200)
                node = (
                    x,
                    y,
                    self.being_culture.value,
                    stratum_num,
                    1,
                    population_center_resource_yeild,
                )

                conn = create_connection(self.db_file)
                create_node(conn, node)
                self.nodes.append(node)

                # generate supporting nodes
                num_support = np.random.randint(min_support, max_support + 1)
                for _ in range(num_support):
                    # controls how close the points are
                    delta = 0.2
                    l = np.random.uniform(length - delta, length + delta)
                    a = np.random.uniform(angle - np.pi / 8, angle + np.pi / 8)

                    x = l * np.cos(a)
                    y = l * np.sin(a)

                    self.ax.scatter(
                        x,
                        y,
                        color=self.colors[color_num],
                        marker=self.markers[i],
                        alpha=0.5,
                        linewidths=0.25,
                    )

                    yeild_delta = 50
                    supporting_node_resource_yeild = np.random.randint(
                        int(population_center_resource_yeild * 0.1),
                        int(population_center_resource_yeild * 0.6),
                    )
                    # 0 for not a population center
                    node = (
                        x,
                        y,
                        self.being_culture.value,
                        stratum_num,
                        0,
                        supporting_node_resource_yeild,
                    )
                    create_node(conn, node)
                    self.nodes.append(node)

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
