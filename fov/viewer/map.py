from pathlib import Path
from fov.common.vector2d import Vector2D


def load_map(path: Path) -> tuple[Vector2D, set[Vector2D]]:
    """Read a map file and parse it with parse_map.

    Returns (player_start, walls). See parse_map for details.
    """
    with open(path) as file:
        map_lines = file.readlines()
    return parse_map(map_lines)


def parse_map(map: list[str]) -> tuple[Vector2D, set[Vector2D]]:
    """Parse map lines, where '#' is a wall and '@' the player start.

    Returns (player_start, walls): the start position and the set of wall
    positions, with x as the column and y as the row index.
    Raises ValueError if there is no '@'.
    """
    walls: set[Vector2D] = set()
    player_pos: Vector2D | None = None

    for y, line in enumerate(map):
        for x, ch in enumerate(line):
            if ch == "@":
                player_pos = Vector2D(x, y)
            elif ch == "#":
                walls.add(Vector2D(x, y))

    if player_pos is None:
        raise ValueError("map has no player start '@'")
    return player_pos, walls
