"""Position value object: (x, y) on the field."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Immutable (x, y) coordinate. Origin (0,0) is bottom-left."""

    x: int
    y: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
