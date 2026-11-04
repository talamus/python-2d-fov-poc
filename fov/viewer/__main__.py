import argparse
import sys
from pathlib import Path

from .fov import load_fov
from .map import load_map
from .ui import start_ui

if __name__ != "__main__":
    raise SystemExit("This needs to be run as a main program")

ASSETS_DIR = Path(__file__).parent.parent / "assets"

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="Test your precalculated field-of-view octants interactively",
    epilog="WASD or arrow key moves, Q or Esc quits"
)
parser.add_argument(
    "-f", "--fov",
    help="field-of-view file to be used",
    default=ASSETS_DIR / "fov_manual_15x15.txt"
)
parser.add_argument(
    "-m", "--map",
    help="map file to be used",
    default=ASSETS_DIR / "map.txt"
)
args = parser.parse_args()

FOV_FILE = Path(args.fov)
MAP_FILE = Path(args.map)
INITIAL_PLAYER_POS, WALLS = load_map(MAP_FILE)
FOV_DIM, FOV_TREE = load_fov(FOV_FILE)

start_ui(INITIAL_PLAYER_POS, WALLS, FOV_DIM, FOV_TREE)
