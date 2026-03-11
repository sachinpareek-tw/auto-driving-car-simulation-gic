"""Unit tests for Direction (rotation logic)."""

import pytest
from src.domain.direction import Direction


def test_rotate_left_from_north() -> None:
    assert Direction.N.rotate_left() == Direction.W


def test_rotate_left_full_cycle() -> None:
    d = Direction.N
    for _ in range(4):
        d = d.rotate_left()
    assert d == Direction.N


def test_rotate_right_from_north() -> None:
    assert Direction.N.rotate_right() == Direction.E


def test_rotate_right_full_cycle() -> None:
    d = Direction.N
    for _ in range(4):
        d = d.rotate_right()
    assert d == Direction.N


def test_rotate_left_all_directions() -> None:
    assert Direction.N.rotate_left() == Direction.W
    assert Direction.W.rotate_left() == Direction.S
    assert Direction.S.rotate_left() == Direction.E
    assert Direction.E.rotate_left() == Direction.N


def test_rotate_right_all_directions() -> None:
    assert Direction.N.rotate_right() == Direction.E
    assert Direction.E.rotate_right() == Direction.S
    assert Direction.S.rotate_right() == Direction.W
    assert Direction.W.rotate_right() == Direction.N
