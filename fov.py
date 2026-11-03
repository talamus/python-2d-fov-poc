from vector2d import Vector2D

# Each row is (xx, xy, yx, yy): maps a tree coordinate (x, y) to the map offset
# (xx*x + xy*y, yx*x + yy*y). Together they cover all eight sectors of the view.
SECTORS = [
    (1, 0, 0, 1),
    (0, 1, 1, 0),
    (0, -1, 1, 0),
    (-1, 0, 0, 1),
    (-1, 0, 0, -1),
    (0, -1, -1, 0),
    (0, 1, -1, 0),
    (1, 0, 0, -1),
]

FoV = {
    (1,0): {
        (2,0): {
            (3,0): {
                (4,0): {
                    (5,0): {
                        (6,0): {
                            (7,0): True
                        }
                    }
                },
                (4,1): {
                    (5,1): {
                        (6,1): {
                            (7,1): True
                        }
                    }
                }
            },
            (3,1): {
                (4,1): True
            }
        },
        (2,1): {
            (3,1): {
                (4,2): {
                    (5,2): {
                        (6,2): {
                            (7,2): True,
                            (7,3): True
                        }
                    }
                }
            }
        }
    },
    (1,1): {
        (2,1): {
            (3,2): {
                (4,2): {
                    (5,3): {
                        (6,3): True
                    }
                },
                (4,3): {
                    (5,3): {
                        (6,4): True
                    }
                }
            }
        },
        (2,2): {
            (3,3): {
                (4,3): {
                    (5,4): {
                        (6,5): True
                    }
                },
                (4,4): {
                    (5,5): True
                }
            }
        }
    }
}


def _walk_sector(tree, origin, sector, walls, visible):
    # A leaf of the tree is True instead of a dict of further cells.
    if tree is True:
        return
    xx, xy, yx, yy = sector
    for (x, y), subtree in tree.items():
        cell = Vector2D(xx*x + xy*y, yx*x + yy*y)
        visible.add(cell)
        # A wall is seen itself, but it hides everything behind it.
        if origin + cell not in walls:
            _walk_sector(subtree, origin, sector, walls, visible)


def calculate_view(origin: Vector2D, walls: set[Vector2D]) -> set[Vector2D]:
    """Return the cells visible from origin, within the 15x15 view."""
    visible = {Vector2D(0, 0)}
    for sector in SECTORS:
        _walk_sector(FoV, origin, sector, walls, visible)
    return visible
