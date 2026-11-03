from vector2d import Vector2D

RAW_MAP = [
    "                                            ",
    "                                            ",
    "                        #####               ",
    "        ##########      #   ########        ",
    "        #        #      #          #        ",
    "        #        #      #   ####   #        ",
    "        #  #     #      #####  #   #        ",
    "        #  #     #   @         #   #        ",
    "        #  #######      ##                  ",
    "                        ##                  ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                           #"
]

def parse_map() -> tuple[Vector2D, set[Vector2D]]:
    walls: set[Vector2D] = set()
    player_pos: Vector2D | None = None

    for y, line in enumerate(RAW_MAP):
        for x, ch in enumerate(line):
            if ch == "@":
                player_pos = Vector2D(x, y)
            elif ch == "#":
                walls.add(Vector2D(x, y))

    if player_pos is None:
        raise ValueError("map has no player start '@'")
    return player_pos, walls

INITIAL_PLAYER_POS, WALLS = parse_map()
