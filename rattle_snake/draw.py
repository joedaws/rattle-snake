import matplotlib.pyplot as plt


def draw_pop_center(ax, x, y, color, marker):
    """Draw a population center on the provided axes"""
    draw_node(ax, x, y, color, 1.0, marker, 3.0)


def draw_support_node(ax, x, y, color, marker):
    """Draw a supporting node on the provided axes"""
    draw_node(ax, x, y, color, 0.25, marker, 0.25)


def draw_node(ax, x, y, color, alpha, marker, linewidths):
    ax.scatter(
        x,
        y,
        color=color,
        alpha=alpha,
        marker=marker,
        linewidths=linewidths,
    )


def draw_edge(ax, x_values, y_values):
    ax.plot(
        x_values,
        y_values,
        alpha=0.5,
        linewidth=0.5,
    )
