import random
from typing import Any
from curses import curs_set, window, wrapper

from fov.common.vector2d import Vector2D
from fov.viewer.fov import FovTree, calculate_view


class BadTerminal(Exception):
    """Raised when the terminal is too small to draw the view."""


def start_ui(*args: Any) -> None:
    """Run the interactive viewer; arguments are passed to _main_loop.

    Returns nothing. A too-small terminal is reported by printing a message.
    """
    try:
        wrapper(_main_loop, *args)
    except BadTerminal as e:
        print(e)


def _main_loop(stdscr: window,
        initial_player_pos: Vector2D,
        walls: set[Vector2D],
        fov_dim: int,
        fov_tree: FovTree
    ) -> None:
    """Draw the view and handle key input until the player quits."""
    max_rows = fov_dim * 2 + 2
    max_cols = fov_dim * 4 + 4
    player_pos = initial_player_pos

    curs_set(0)
    stdscr.clear()

    for i in range(0, fov_dim + 1):
        x_mark = i % 10 or "|"
        y_mark = i % 10 or "-"
        stdscr.addstr(max_rows - 1, 2 * fov_dim + 2 * i + 1, str(x_mark))
        stdscr.addstr(fov_dim + i, max_cols, str(y_mark))

    while True:
        rows, cols = stdscr.getmaxyx()
        if rows <= max_rows or cols <= max_cols:
            raise BadTerminal(f"Terminal too small: need {max_cols}x{max_cols}, have {cols}x{rows}")

        visible = calculate_view(fov_tree, player_pos, walls)
        for y in range(-fov_dim, fov_dim + 1):
            line = ""
            for x in range(-fov_dim, fov_dim + 1):
                cell = "  "
                if Vector2D(x, y) in visible:
                    cell = ".."
                    if player_pos + Vector2D(x, y) in walls:
                        cell = "##"
                if Vector2D(x, y) == Vector2D(0, 0):
                    cell = "()"
                line += cell
            stdscr.addstr(y + fov_dim, 1, line)
        stdscr.refresh()

        delta = Vector2D(0, 0)
        match stdscr.getkey():
            case "w" | "KEY_UP":
                delta = Vector2D(0, -1)
            case "a" | "KEY_LEFT":
                delta = Vector2D(-1, 0)
            case "s" | "KEY_DOWN":
                delta = Vector2D(0, 1)
            case "d" | "KEY_RIGHT":
                delta = Vector2D(1, 0)
            case "q" | "KEY_EXIT" | "\x1b":
                return
        new_player_pos = player_pos + delta
        if new_player_pos not in walls:
            player_pos = new_player_pos
