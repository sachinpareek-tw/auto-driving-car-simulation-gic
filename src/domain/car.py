"""Car: name, position, direction, and command string (L/R/F)."""

from dataclasses import dataclass
from typing import Optional

from src.domain.direction import Direction
from src.domain.field import Field
from src.domain.position import Position


# Command characters
CMD_LEFT = "L"
CMD_RIGHT = "R"
CMD_FORWARD = "F"


@dataclass(frozen=True)
class CommandResult:
    """Result of executing one command: position for collision grid, and updated car if move applied."""

    position: Position
    updated_car: Optional["Car"]


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

    def execute_command(self, cmd: Optional[str], field: Field) -> CommandResult:
        """
        Execute one command (L/R/F or None). Returns position and updated car if move applied.
        Domain logic: rotation, forward with bounds check.
        """
        if cmd is None or cmd not in (CMD_LEFT, CMD_RIGHT, CMD_FORWARD):
            return CommandResult(position=self.position, updated_car=None)
        if cmd == CMD_LEFT:
            return CommandResult(position=self.position, updated_car=self.with_rotation_left())
        if cmd == CMD_RIGHT:
            return CommandResult(position=self.position, updated_car=self.with_rotation_right())
        # cmd == CMD_FORWARD
        next_pos = self.position_after_forward()
        if field.is_within_bounds(next_pos):
            return CommandResult(position=next_pos, updated_car=self.with_position(next_pos))
        return CommandResult(position=self.position, updated_car=None)
