"""
draw the concentric circles
"""
import matplotlib.pyplot as plt
import numpy as np

from rattle_snake.constants import BeingCulture
from rattle_snake.db_helpers import db_setup, create_node, create_connection


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
        self, being_culture: str, num_circles: int = 4, create_new_nodes: bool = True
    ):
        """
        Args:
            being_culture (str): One of "weird_science", "dream_realm", "deep_denizen"
            num_circles (int): Number of tiered circles to draw
        """
        # ensure that the database is ready to go
        db_setup()
        self.being_culture = BeingCulture(being_culture)
        self.num_circles = num_circles
        # nodes setup
        self.stratum_radii = 2.0
        self.stratum_boundaries = [
            ((i) * self.stratum_radii, (i + 1) * self.stratum_radii)
            for i in range(num_circles)
        ]

        # plotting setup
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect(1)
        self.title = self.map_file_names[self.being_culture]
        plt.title(self.title)

        # this populates the nodes table
        if create_new_nodes:
            self.generate_nodes()

    def save(self):
        """Save an image of the map in is current state"""
        plt.savefig(self.title)

    def generate_nodes(self, k: int = 3, min_support: int = 3, max_support: int = 10):
        """Generate the nodes.

        There are k population centers in each stratum.
        For each population center we generate a random nubmer of
        supporting/surround nodes.
        """
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
                node = (x, y, stratum_num, 1, population_center_resource_yeild)

                conn = create_connection()
                create_node(conn, node)

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
                    node = (x, y, stratum_num, 0, supporting_node_resource_yeild)
                    create_node(conn, node)

    def draw_circles(self):
        """Draw the domain of the weird science beings"""
        angle = np.linspace(0, 2 * np.pi, 250)

        for i in range(self.num_circles):
            radius = (i + 1) * self.stratum_radii

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # draw a circle
            self.ax.plot(x, y, color="gray")

    def draw(self):
        """Draw everyting for this realm map"""
        self.draw_circles()
        # TODO replace with a load nodes from the database
        self.generate_nodes()


def main():
    plane_map = PlaneMap(being_culture="weird_science")
    plane_map.draw()
    plane_map.save()

    print("Drawing Complete")


if __name__ == "__main__":
    main()
