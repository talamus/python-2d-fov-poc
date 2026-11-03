from curses import wrapper, window
from fov import calculate_view
from vector2d import Vector2D
from map import INITIAL_PLAYER_POS, WALLS

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

        for x in range(player_pos.x - 7, player_pos.x + 8):
            for y in range(player_pos.y - 7, player_pos.y + 8):
                environment = "  "
                if Vector2D(x,y) in visible:
                    environment = ".."
                    if Vector2D(x,y) in WALLS:
                        environment = "##"
                if Vector2D(x,y) == player_pos:
                    environment = "()"
                stdscr.addstr(7 + y - player_pos.y, 2*(7 + x - player_pos.x), environment)
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
