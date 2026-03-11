"""Unit tests for Position."""

import pytest
from src.domain.position import Position


def test_position_equality() -> None:
    assert Position(0, 0) == Position(0, 0)
    assert Position(1, 2) == Position(1, 2)
    assert Position(1, 2) != Position(1, 3)
    assert Position(1, 2) != Position(3, 2)


def test_position_hash() -> None:
    assert hash(Position(1, 2)) == hash(Position(1, 2))
    d = {Position(0, 0): "origin"}
    assert d[Position(0, 0)] == "origin"
