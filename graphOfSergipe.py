# %% [markdown]
# I have used a tool called ogr2ogr to convert the original json
#
# with uses coordinates with WGS84(EPSG:4326) to projection (EPSG:31983)
#
# Commands: ogr2ogr -f "GeoJSON" -t_srs "EPSG:31983" sergipeEPSG31983.geojson sergipe.json
#
# Github of the original JSON: https://github.com/giuliano-macedo/geodata-br-states
#
# EPSG:4326: https://epsg.io/4326
#
# EPSG:31983: https://epsg.io/31983

# %% [markdown]
# Import the necessary library's

# %%
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
from typing import Tuple
import math

# %% [markdown]
# Extract the points from the geojson

# %%
fileName = "sergipeEPSG31983"
d = json.load(open(f"./{fileName}.geojson"))
points = d["features"][0]["geometry"]["coordinates"][0][0]


# %% [markdown]
# Generate the coordinates of Sergipe perimeter

# %%
OFFSET_X_WEIGHT = 1.34e6
OFFSET_Y_WEIGHT = 8.80e6
x = [(point[0] - OFFSET_X_WEIGHT) / 1e4 for point in points]
y = [(point[1] - OFFSET_Y_WEIGHT) / 1e4 for point in points]


# %%
def is_point_in_rectangle(p, a, b, c, d):
    """
    Check if point p is inside rectangle defined by points a, b, c, d
    Points should be in clockwise or counter-clockwise order
    """

    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])

    # Check if point is on the same side of all edges
    d1 = cross_product(a, b, p)
    d2 = cross_product(b, c, p)
    d3 = cross_product(c, d, p)
    d4 = cross_product(d, a, p)

    # Point is inside if all cross products have the same sign
    return (d1 >= 0 and d2 >= 0 and d3 >= 0 and d4 >= 0) or (
        d1 <= 0 and d2 <= 0 and d3 <= 0 and d4 <= 0
    )


if __name__ == "__main__":
    is_point_in_rectangle((2.5, 2), (0, 0), (0, 5), (5, 5), (5, 0))


# %%
def round_value(value: float, multiple=10000) -> int:
    return math.floor(value / multiple) * multiple


def round_down_point_to_multiple(point: Tuple[float, float], multiple=10000):
    """
    Round down a value to the nearest multiple of the specified number.

    Args:
        value: The number to round down
        multiple: The multiple to round down to (default: 10000)

    Returns:
        The largest multiple that is less than or equal to value

    Examples:
        >>> round_down_to_multiple(15000)
        10000
        >>> round_down_to_multiple(-5000)
        -10000
        >>> round_down_to_multiple(0)
        0
        >>> round_down_to_multiple(10000)
        10000
    """
    return (round_value(point[0], multiple), round_value(point[1], multiple))


# Test examples
if __name__ == "__main__":
    print(round_down_point_to_multiple((15000, -5000)))

# %% [markdown]
# Square Locations in the perimeter

# %%
square_points = list(
    set(
        round_down_point_to_multiple((x[index], y[index]), 1)
        for index in range(0, len(x))
    )
)
# list(map(lambda x: (x[0]/1e4, x[1]/1e4), square_points))

# %% [markdown]
# Graph Configuration

# %%
# Create figure and axis with better size
fig, ax = plt.subplots(figsize=(10, 8))
line = ax.plot(x, y, linewidth=2, label="Sergipe", color="#2E86AB")
# Set up the grid with more divisions
ax.grid(True, which="both", linestyle="-", linewidth=0.7, alpha=0.7)
# Add minor grid lines for more divisions
ax.minorticks_on()
ax.grid(True, which="minor", linestyle="-", linewidth=0.7, alpha=0.7)
# Add axes at (0,0)
ax.axhline(y=0, color="k", linewidth=0.5)
ax.axvline(x=0, color="k", linewidth=0.5)
# Major ticks every 50,000
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
# Minor ticks every 10,000
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(1))
# Add labels and title
ax.set_xlabel("X Values", fontsize=12)
ax.set_ylabel("Y Values", fontsize=12)
ax.set_title("Sergipe Data Visualization", fontsize=14, fontweight="bold")
# Add legend
ax.legend(loc="best", frameon=True, fancybox=True, shadow=True)
# Improve tick formatting
ax.tick_params(axis="both", which="major", labelsize=10)
# Adjust layout to prevent clipping
plt.tight_layout()
ax.set_aspect(1)
# Add red rectangle at (0, 0)
for point in square_points:
    rect_width = 1  # ajuste conforme necessário
    rect_height = 1  # ajuste conforme necessário
    rectangle = Rectangle(
        (point),
        rect_width,
        rect_height,
        linewidth=2,
        edgecolor="red",
        facecolor="lightcoral",
        alpha=0.5,
    )
    ax.add_patch(rectangle)
# Add scale bar
scale_length = 5  # Length in plot units (5 km)
scale_x = min(x) + 15  # Position from left
scale_y = min(y) + 1  # Position from bottom

# Draw scale bar
ax.plot(
    [scale_x, scale_x + scale_length], [scale_y, scale_y], color="black", linewidth=3
)
# Add scale bar end marks
ax.plot([scale_x, scale_x], [scale_y - 0.2, scale_y + 0.2], color="black", linewidth=2)
ax.plot(
    [scale_x + scale_length, scale_x + scale_length],
    [scale_y - 0.2, scale_y + 0.2],
    color="black",
    linewidth=2,
)
# Add scale text
ax.text(
    scale_x + scale_length / 2,
    scale_y - 0.5,
    f"{scale_length * 10:.0f} km",
    ha="center",
    va="top",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
)
# plot the graph
plt.show()

# %%
