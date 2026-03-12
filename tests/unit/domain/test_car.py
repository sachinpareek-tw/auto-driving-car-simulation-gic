"""Unit tests for Car (move F, rotate L/R, command at step, execute_command)."""

import pytest
from src.domain.car import Car, CommandResult, CMD_LEFT, CMD_RIGHT, CMD_FORWARD
from src.domain.direction import Direction
from src.domain.field import Field
from src.domain.position import Position


def test_car_position_after_forward_north() -> None:
    car = Car("A", Position(1, 2), Direction.N, "F")
    assert car.position_after_forward() == Position(1, 3)


def test_car_position_after_forward_south() -> None:
    car = Car("A", Position(1, 2), Direction.S, "F")
    assert car.position_after_forward() == Position(1, 1)


def test_car_position_after_forward_east() -> None:
    car = Car("A", Position(1, 2), Direction.E, "F")
    assert car.position_after_forward() == Position(2, 2)


def test_car_position_after_forward_west() -> None:
    car = Car("A", Position(1, 2), Direction.W, "F")
    assert car.position_after_forward() == Position(0, 2)


def test_car_rotate_left() -> None:
    car = Car("A", Position(1, 2), Direction.N, "L")
    new_car = car.with_rotation_left()
    assert new_car.direction == Direction.W
    assert new_car.position == Position(1, 2)


def test_car_rotate_right() -> None:
    car = Car("A", Position(1, 2), Direction.N, "R")
    new_car = car.with_rotation_right()
    assert new_car.direction == Direction.E
    assert new_car.position == Position(1, 2)


def test_car_with_position() -> None:
    car = Car("A", Position(1, 2), Direction.N, "FF")
    new_car = car.with_position(Position(5, 4))
    assert new_car.position == Position(5, 4)
    assert new_car.direction == Direction.N
    assert new_car.name == "A"


def test_car_get_command_at_step() -> None:
    car = Car("A", Position(0, 0), Direction.N, "FFRFFFFRRL")
    assert car.get_command_at_step(0) == CMD_FORWARD
    assert car.get_command_at_step(1) == CMD_FORWARD
    assert car.get_command_at_step(2) == CMD_RIGHT
    assert car.get_command_at_step(9) == CMD_LEFT
    assert car.get_command_at_step(10) is None
    assert car.get_command_at_step(-1) is None


def test_execute_command_none() -> None:
    field = Field(5, 5)
    car = Car("A", Position(1, 2), Direction.N, "F")
    result = car.execute_command(None, field)
    assert result.position == Position(1, 2)
    assert result.updated_car is None


def test_execute_command_left() -> None:
    field = Field(5, 5)
    car = Car("A", Position(1, 2), Direction.N, "L")
    result = car.execute_command(CMD_LEFT, field)
    assert result.position == Position(1, 2)
    assert result.updated_car is not None
    assert result.updated_car.direction == Direction.W
    assert result.updated_car.position == Position(1, 2)


def test_execute_command_right() -> None:
    field = Field(5, 5)
    car = Car("A", Position(1, 2), Direction.N, "R")
    result = car.execute_command(CMD_RIGHT, field)
    assert result.position == Position(1, 2)
    assert result.updated_car is not None
    assert result.updated_car.direction == Direction.E


def test_execute_command_forward_in_bounds() -> None:
    field = Field(5, 5)
    car = Car("A", Position(1, 2), Direction.N, "F")
    result = car.execute_command(CMD_FORWARD, field)
    assert result.position == Position(1, 3)
    assert result.updated_car is not None
    assert result.updated_car.position == Position(1, 3)


def test_execute_command_forward_out_of_bounds() -> None:
    field = Field(3, 3)  # x,y in [0,2]
    car = Car("A", Position(1, 2), Direction.N, "F")  # forward would go to (1,3)
    result = car.execute_command(CMD_FORWARD, field)
    assert result.position == Position(1, 2)
    assert result.updated_car is None
