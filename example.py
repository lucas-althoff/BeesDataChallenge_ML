import random
from typing import List

from fuel_efficiency.algorithms.a_star import AStarStrategy
from fuel_efficiency.algorithms.context import Context
from fuel_efficiency.algorithms.dijkstra import DijkstraStrategy
from fuel_efficiency.entities.down_hill import DownHill
from fuel_efficiency.entities.plateau import Plateau
from fuel_efficiency.entities.position import Position
from fuel_efficiency.entities.up_hill import UpHill
from fuel_efficiency.entities.valley import Valley


def generate_terrain(prev_terrain=None):
    """Generate a random terrain type based on continuity rules."""
    terrain_types = [Valley, UpHill, DownHill, Plateau]

    if prev_terrain == UpHill:
        # If the previous terrain is UpHill,
        # the next terrain cannot be Valley
        terrain_types.remove(Valley)
    elif prev_terrain == DownHill:
        # If the previous terrain is DownHill,
        # the next terrain cannot be Plateau
        terrain_types.remove(Plateau)

    return random.choice(terrain_types)


def get_random_edge_position(N: int, M: int) -> Position:
    """Select a random position from the edge of the grid."""
    edge_positions = (
        [(x, 0) for x in range(N)]
        + [(x, M - 1) for x in range(N)]
        + [(0, y) for y in range(1, M - 1)]
        + [(N - 1, y) for y in range(1, M - 1)]
    )
    x, y = random.choice(edge_positions)
    return Position(x, y)  # pragma: no cover


def create_grid(N: int, M: int) -> List[List[object]]:
    """
    Create an NxM grid with random terrain types, adhering to continuity rules.

    Args:
        N (int): Number of rows in the grid.
        M (int): Number of columns in the grid.

    Returns:
        List[List[object]]: An NxM grid populated with terrain objects.
    """
    grid = []
    prev_terrain = None

    for x in range(N):
        row = []
        for y in range(M):
            terrain_type = generate_terrain(prev_terrain)
            prev_terrain = terrain_type
            row.append(terrain_type(position=Position(x, y)))
        grid.append(row)

    return grid  # pragma: no cover


def print_grid(grid: List[List[object]]):
    """Print the grid with visual representation."""
    symbols = {Valley: 'V', UpHill: 'U', DownHill: 'D', Plateau: 'P'}

    for row in grid:
        print(
            ' '.join(symbols[type(cell)] for cell in row)
        )  # pragma: no cover


if __name__ == '__main__':
    grid = create_grid(10, 10)

    print_grid(grid)

    start_position = get_random_edge_position(10, 10)
    end_position = get_random_edge_position(10, 10)

    while start_position == end_position:
        end_position = get_random_edge_position(10, 10)

    start = Valley(position=start_position)
    end = Valley(position=end_position)

    print('\n=========  START  =========\n', start.position)
    print('\n=========  END  =========\n', end.position)

    context = Context()
    context.grid = grid
    context.start = start
    context.end = end

    context.strategy = AStarStrategy()
    path = context.run()

    print('\n=========  A* Solution  =========\n', path)

    context.strategy = DijkstraStrategy()
    path = context.run()
    print("\n=========  Djikstra's Solution  =========\n", path)
