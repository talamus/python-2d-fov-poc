import argparse
import sys
from fractions import Fraction
from pathlib import Path

from .rays import FULL_CELL, Cell, generate_octant

if __name__ != "__main__":
    raise SystemExit("This needs to be run as a main program")

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="Generate a new field-of-view octant file"
)
parser.add_argument(
    "-o", "--output",
    help="output file for the octant (default: standard output)",
    type=Path,
)
parser.add_argument(
    "-s", "--size",
    help="size of the octant (default: %(default)s, a 15x15 area)",
    type=int,
    default=7
)
parser.add_argument(
    "-c", "--circle",
    help="circularize the octant",
    action="store_true"
)
parser.add_argument(
    "--circle-margin",
    help="added to the size to get the circle's radius (default: %(default)s)",
    type=Fraction,
    default=Fraction(1, 2)
)
parser.add_argument(
    "--cell-margin",
    help="how far from the centre of its end cells a ray may pass, from 0 to "
         "1/2. Less means fewer rays, but also that walls start to go missing "
         "along corridors and rooms (default: %(default)s)",
    type=Fraction,
    default=FULL_CELL
)
args = parser.parse_args()

if args.size < 1:
    parser.error("size must be at least 1")
if not 0 <= args.cell_margin <= FULL_CELL:
    parser.error("cell margin must be from 0 to 1/2")
if args.size + args.circle_margin < 1:
    parser.error("circle is too small to contain any cells")

radius = args.size + args.circle_margin


def contains(cell: Cell) -> bool:
    """Tell if a cell belongs to the area of the octant."""
    x, y = cell
    return x <= args.size and (not args.circle or x * x + y * y <= radius * radius)


rays = generate_octant(contains, args.cell_margin)

full_size = args.size * 2 + 1
if args.circle:
    area = f"{full_size}x{full_size} (circle, radius {float(radius)})"
else:
    area = f"{full_size}x{full_size} (square)"

lines = [
    "# Generated field-of-view octant",
    f"# Full area: {area}",
    f"# Cell margin: {args.cell_margin}",
    "",
    *(" ".join(f"{x},{y}" for x, y in ray) for ray in rays),
]
text = "\n".join(lines) + "\n"

if args.output is None:
    sys.stdout.write(text)
else:
    args.output.write_text(text)
