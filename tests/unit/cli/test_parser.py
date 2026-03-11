"""Unit tests for CLI parser."""

import pytest
from src.domain.direction import Direction
from src.domain.position import Position
from src.cli.parser import parse_field_dimensions, parse_position_direction, parse_commands


def test_parse_field_dimensions_valid() -> None:
    assert parse_field_dimensions("10 10") == (10, 10)
    assert parse_field_dimensions("  5  3  ") == (5, 3)


def test_parse_field_dimensions_invalid() -> None:
    assert parse_field_dimensions("10") is None
    assert parse_field_dimensions("10 10 10") is None
    assert parse_field_dimensions("x y") is None
    assert parse_field_dimensions("0 10") is None
    assert parse_field_dimensions("10 0") is None


def test_parse_position_direction_valid() -> None:
    assert parse_position_direction("1 2 N") == (Position(1, 2), Direction.N)
    assert parse_position_direction("7 8 W") == (Position(7, 8), Direction.W)
    assert parse_position_direction("  0  0  S  ") == (Position(0, 0), Direction.S)


def test_parse_position_direction_invalid() -> None:
    assert parse_position_direction("1 2") is None
    assert parse_position_direction("1 2 X") is None
    assert parse_position_direction("a 2 N") is None


def test_parse_commands() -> None:
    assert parse_commands("FFRFFFFRRL") == "FFRFFFFRRL"
    assert parse_commands("  F F  ") == "F F"
