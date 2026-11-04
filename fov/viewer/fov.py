from pathlib import Path
from typing import Literal, TypeAlias

from fov.common.vector2d import Vector2D

# Each row is (xx, xy, yx, yy): maps a tree coordinate (x, y) to the map offset
# (xx*x + xy*y, yx*x + yy*y). Together they cover all eight sectors of the view.
SECTORS: list[tuple[int, int, int, int]] = [
    (1, 0, 0, 1),
    (0, 1, 1, 0),
    (0, -1, 1, 0),
    (-1, 0, 0, 1),
    (-1, 0, 0, -1),
    (0, -1, -1, 0),
    (0, 1, -1, 0),
    (1, 0, 0, -1),
]

# A tree of cells: each key is a coordinate (x, y) in the first sector, and the
# value is the subtree of cells behind it, or True at a leaf.
Cell: TypeAlias = tuple[int, int]
FovTree: TypeAlias = dict[Cell, "FovTree | Literal[True]"]


def load_fov(path: Path) -> tuple[int, FovTree]:
    """Load a field-of-view tree from a text file.

    Each line is a chain of "x,y" cells ending in a leaf; '#' starts a comment.
    Returns (max_dim, tree): the length of the longest chain, and the FovTree.
    """
    fov: FovTree = {}
    max_dim: int = 0

    with open(path) as input:
        for line in input:

            # Strip comments and ignore empty lines
            line = line.split("#")[0].strip()
            if not line:
                continue

            cells: list[Cell] = []
            for c in line.split():
                x, y = map(int, c.split(","))
                cells.append((x, y))
            max_dim = max(max_dim, len(cells))

            node: FovTree = fov
            for cell in cells[:-1]:
                child = node.setdefault(cell, {})
                assert isinstance(child, dict)
                node = child
            node[cells[-1]] = True

    return max_dim, fov


def _walk_sector(
    fov_tree: FovTree | Literal[True],
    origin: Vector2D,
    sector: tuple[int, int, int, int],
    walls: set[Vector2D],
    visible_cells: set[Vector2D],
) -> None:
    """Add the cells visible in one sector to visible_cells (in place)."""

    # A leaf of the tree is True instead of a dict of further cells.
    if fov_tree is True:
        return

    xx, xy, yx, yy = sector
    for (x, y), subtree in fov_tree.items():
        cell = Vector2D(xx*x + xy*y, yx*x + yy*y)
        visible_cells.add(cell)
        # A wall is seen itself, but it hides everything behind it.
        if origin + cell not in walls:
            _walk_sector(subtree, origin, sector, walls, visible_cells)


def calculate_view(fov_tree: FovTree, origin: Vector2D, walls: set[Vector2D]) -> set[Vector2D]:
    """Calculate which cells are visible from origin.

    Returns a set of Vector2D offsets relative to origin (not map positions),
    always including (0, 0). Walls that are seen are included.
    """
    visible_cells = {Vector2D(0, 0)}
    for sector in SECTORS:
        _walk_sector(fov_tree, origin, sector, walls, visible_cells)
    return visible_cells
