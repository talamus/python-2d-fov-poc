from curses import window, wrapper

from fov import calculate_view
from map import INITIAL_PLAYER_POS, WALLS
from vector2d import Vector2D

# The view is 15 cells of 2 columns each. One extra column is needed because
# curses raises an error after writing to the bottom-right corner of the screen.
MIN_ROWS = 15
MIN_COLS = 2 * 15 + 1


class BadTerminal(Exception):
    pass


def main(stdscr: window) -> None:
    stdscr.clear()
    player_pos = INITIAL_PLAYER_POS

    while True:
        rows, cols = stdscr.getmaxyx()
        if rows < MIN_ROWS or cols < MIN_COLS:
            raise BadTerminal(f"Terminal too small: need {MIN_COLS}x{MIN_ROWS}, have {cols}x{rows}")

        visible = calculate_view(player_pos, WALLS)
        for y in range(-7, 7):
            line = ""
            for x in range(-7, 7):
                block = "  "
                if Vector2D(x, y) in visible:
                    block = ".."
                    if player_pos + Vector2D(x, y) in WALLS:
                        block = "##"
                if Vector2D(x, y) == Vector2D(0, 0):
                    block = "()"
                line += block
            stdscr.addstr(y + 7, 1, line)
        stdscr.refresh()

        delta = Vector2D(0, 0)
        match stdscr.getkey():
            case "w":
                delta = Vector2D(0, -1)
            case "a":
                delta = Vector2D(-1, 0)
            case "s":
                delta = Vector2D(0, 1)
            case "d":
                delta = Vector2D(1, 0)
            case "q":
                return
        new_player_pos = player_pos + delta
        if new_player_pos not in WALLS:
            player_pos = new_player_pos


if __name__ == "__main__":
    try:
        wrapper(main)
    except BadTerminal as e:
        print(e)
