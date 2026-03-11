"""Unit tests for Field (bounds check)."""

import pytest
from src.domain.field import Field
from src.domain.position import Position


def test_field_valid_dimensions() -> None:
    f = Field(10, 10)
    assert f.width == 10
    assert f.height == 10


def test_field_is_within_bounds_inside() -> None:
    f = Field(10, 10)
    assert f.is_within_bounds(Position(0, 0)) is True
    assert f.is_within_bounds(Position(9, 9)) is True
    assert f.is_within_bounds(Position(5, 5)) is True


def test_field_is_within_bounds_outside_x_low() -> None:
    f = Field(10, 10)
    assert f.is_within_bounds(Position(-1, 5)) is False


def test_field_is_within_bounds_outside_x_high() -> None:
    f = Field(10, 10)
    assert f.is_within_bounds(Position(10, 5)) is False


def test_field_is_within_bounds_outside_y_low() -> None:
    f = Field(10, 10)
    assert f.is_within_bounds(Position(5, -1)) is False


def test_field_is_within_bounds_outside_y_high() -> None:
    f = Field(10, 10)
    assert f.is_within_bounds(Position(5, 10)) is False


def test_field_invalid_width_raises() -> None:
    with pytest.raises(ValueError, match="width and height must be positive"):
        Field(0, 10)


def test_field_invalid_height_raises() -> None:
    with pytest.raises(ValueError, match="width and height must be positive"):
        Field(10, 0)
