"""Field: rectangular area with width and height. Bounds [0, width-1] x [0, height-1]."""

from dataclasses import dataclass

from src.domain.position import Position


@dataclass(frozen=True)
class Field:
    """Rectangular field. Bottom-left is (0,0), top-right is (width-1, height-1)."""

    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width < 1 or self.height < 1:
            raise ValueError("Field width and height must be positive")

    def is_within_bounds(self, position: Position) -> bool:
        """Return True if position is inside the field (inclusive)."""
        return (
            0 <= position.x < self.width
            and 0 <= position.y < self.height
        )
