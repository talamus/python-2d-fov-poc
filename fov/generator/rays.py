"""Generate the rays of a reversible field-of-view octant.

A ray is a chain of cells leaving the origin, and a viewer walks it until it
hits a wall. Reversibility ("if I can see you, you can see me") then asks for
this: whenever a chain reaches a cell, the same chain walked backwards from
that cell has to exist too. As every prefix of a ray is itself a chain to some
cell, a reversed ray can start with any part of the original, so the rays must
hold every piece of every ray, in both directions. `close_rays` ensures this.

Rays are handled as steps, which makes such pieces easy to compare no matter
where they are: from (x, y), step 0 goes to (x+1, y) and step 1 to (x+1, y+1).
"""
from collections.abc import Callable, Iterable
from fractions import Fraction
from itertools import accumulate, combinations

type Cell = tuple[int, int]
type Steps = tuple[int, ...]

FULL_CELL = Fraction(1, 2)


def is_straight(steps: Steps) -> bool:
    """Tell if steps are a digital straight line.

    True when any two stretches of equal length climb within 1 of each other.
    """
    heights = list(accumulate(steps, initial=0))
    for length in range(1, len(steps)):
        climbs = [b - a for a, b in zip(heights, heights[length:])]
        if max(climbs) - min(climbs) > 1:
            return False
    return True


def fits_margin(steps: Steps, cell_margin: Fraction) -> bool:
    """Tell if a line can follow steps within cell_margin of both end centres.

    On the way, the line just has to stay inside each cell. Eliminating the
    line's offset leaves one bound on its slope per pair of columns, so a line
    exists exactly when these bounds do not contradict each other.
    """
    heights = list(accumulate(steps, initial=0))
    reach = [FULL_CELL] * len(heights)
    reach[0] = reach[-1] = cell_margin

    columns = list(combinations(range(len(heights)), 2))
    min_slope = max(
        (heights[j] - reach[j] - heights[i] - reach[i]) / (j - i) for i, j in columns
    )
    max_slope = min(
        (heights[j] + reach[j] - heights[i] + reach[i]) / (j - i) for i, j in columns
    )
    return min_slope <= max_slope


def straight_rays(contains: Callable[[Cell], bool]) -> set[Steps]:
    """Find every straight ray that stays on the cells accepted by contains.

    contains has to accept all the cells of the octant between the origin and
    any cell it accepts, as anything behind a rejected cell is left unexplored.
    """
    rays: set[Steps] = set()
    frontier: list[Steps] = [()]
    while frontier:
        steps = frontier.pop()
        for step in (0, 1):
            ray = (*steps, step)
            if contains((len(ray), sum(ray))) and is_straight(ray):
                rays.add(ray)
                frontier.append(ray)
    return rays


def close_rays(rays: Iterable[Steps]) -> set[Steps]:
    """Add every piece of every ray in both directions, making them reversible."""
    closed: set[Steps] = set()
    for ray in rays:
        for start, end in combinations(range(len(ray) + 1), 2):
            piece = ray[start:end]
            closed.add(piece)
            closed.add(piece[::-1])
    return closed


def longest_rays(rays: set[Steps]) -> set[Steps]:
    """Drop the rays that are just prefixes of other rays."""
    return rays - {ray[:-1] for ray in rays}


def to_cells(ray: Steps) -> list[Cell]:
    """Convert steps into the cells they visit, leaving out the origin."""
    return [(x, y) for x, y in enumerate(accumulate(ray), start=1)]


def generate_octant(
    contains: Callable[[Cell], bool],
    cell_margin: Fraction = FULL_CELL,
) -> list[list[Cell]]:
    """Generate the sorted rays of a reversible octant, as chains of cells.

    See straight_rays for contains. cell_margin, from 0 to 1/2, is how far from
    the centre of the first and last cell a ray may pass. With 1/2 all straight
    rays are in; less gives fewer rays and a narrower view.
    """
    rays = {ray for ray in straight_rays(contains) if fits_margin(ray, cell_margin)}
    return sorted(to_cells(ray) for ray in longest_rays(close_rays(rays)))
