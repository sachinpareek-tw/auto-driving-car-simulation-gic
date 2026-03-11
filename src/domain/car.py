"""Car: name, position, direction, and command string (L/R/F)."""

from dataclasses import dataclass
from typing import Optional

from src.domain.position import Position
from src.domain.direction import Direction


# Command characters
CMD_LEFT = "L"
CMD_RIGHT = "R"
CMD_FORWARD = "F"


@dataclass(frozen=True)
class Car:
    """Immutable car state: name, current position, direction, and full command string."""

    name: str
    position: Position
    direction: Direction
    commands: str

    def get_command_at_step(self, step: int) -> Optional[str]:
        """Return the command at given step (0-based), or None if no command (stay put)."""
        if step < 0 or step >= len(self.commands):
            return None
        c = self.commands[step]
        if c in (CMD_LEFT, CMD_RIGHT, CMD_FORWARD):
            return c
        return None

    def position_after_forward(self) -> Position:
        """Return the position one step forward in current direction (no bounds check)."""
        x, y = self.position.x, self.position.y
        if self.direction == Direction.N:
            return Position(x, y + 1)
        if self.direction == Direction.S:
            return Position(x, y - 1)
        if self.direction == Direction.E:
            return Position(x + 1, y)
        # Direction.W
        return Position(x - 1, y)

    def with_rotation_left(self) -> "Car":
        """Return a new car with direction rotated 90 degrees left."""
        return Car(
            name=self.name,
            position=self.position,
            direction=self.direction.rotate_left(),
            commands=self.commands,
        )

    def with_rotation_right(self) -> "Car":
        """Return a new car with direction rotated 90 degrees right."""
        return Car(
            name=self.name,
            position=self.position,
            direction=self.direction.rotate_right(),
            commands=self.commands,
        )

    def with_position(self, position: Position) -> "Car":
        """Return a new car with the given position."""
        return Car(
            name=self.name,
            position=position,
            direction=self.direction,
            commands=self.commands,
        )
