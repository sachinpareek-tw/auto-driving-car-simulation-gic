"""CLI input parsing: field dimensions, position+direction, command string."""

from typing import Optional, Tuple

from src.domain.direction import Direction
from src.domain.position import Position

VALID_DIRECTIONS = {"N", "S", "E", "W"}


def parse_field_dimensions(line: str) -> Optional[Tuple[int, int]]:
    """Parse 'width height' (e.g. '10 10'). Returns (width, height) or None."""
    parts = line.strip().split()
    if len(parts) != 2:
        return None
    try:
        w, h = int(parts[0]), int(parts[1])
        if w < 1 or h < 1:
            return None
        return (w, h)
    except ValueError:
        return None


def parse_position_direction(line: str) -> Optional[Tuple[Position, Direction]]:
    """Parse 'x y D' (e.g. '1 2 N'). Returns (Position, Direction) or None."""
    parts = line.strip().split()
    if len(parts) != 3:
        return None
    try:
        x, y = int(parts[0]), int(parts[1])
        d = parts[2].upper()
        if d not in VALID_DIRECTIONS:
            return None
        return (Position(x, y), Direction(d))
    except (ValueError, KeyError):
        return None


def parse_commands(line: str) -> str:
    """Return trimmed command string (only L/R/F are valid; store as-is for engine)."""
    return line.strip()
