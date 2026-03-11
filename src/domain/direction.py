"""Direction enum: N, S, E, W with rotation logic."""

from enum import Enum


class Direction(str, Enum):
    """Cardinal direction. N=North, S=South, E=East, W=West."""

    N = "N"
    S = "S"
    E = "E"
    W = "W"

    def rotate_left(self) -> "Direction":
        """Rotate 90 degrees left. N -> W -> S -> E -> N."""
        return _ROTATE_LEFT[self]

    def rotate_right(self) -> "Direction":
        """Rotate 90 degrees right. N -> E -> S -> W -> N."""
        return _ROTATE_RIGHT[self]


_ROTATE_LEFT = {
    Direction.N: Direction.W,
    Direction.W: Direction.S,
    Direction.S: Direction.E,
    Direction.E: Direction.N,
}

_ROTATE_RIGHT = {
    Direction.N: Direction.E,
    Direction.E: Direction.S,
    Direction.S: Direction.W,
    Direction.W: Direction.N,
}
