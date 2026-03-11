"""Unit tests for application use cases."""

import pytest
from src.domain.car import Car
from src.domain.direction import Direction
from src.domain.field import Field
from src.domain.position import Position
from src.application.use_cases import create_field, add_car, run_simulation


def test_create_field() -> None:
    f = create_field(10, 10)
    assert f.width == 10
    assert f.height == 10


def test_create_field_invalid_raises() -> None:
    with pytest.raises(ValueError):
        create_field(0, 10)


def test_add_car_success() -> None:
    field = Field(10, 10)
    cars: list[Car] = []
    new_cars, err = add_car(
        field, cars, "A", Position(1, 2), Direction.N, "FF"
    )
    assert err is None
    assert new_cars is not None
    assert len(new_cars) == 1
    assert new_cars[0].name == "A"
    assert new_cars[0].position == Position(1, 2)
    assert new_cars[0].direction == Direction.N
    assert new_cars[0].commands == "FF"


def test_add_car_duplicate_name_rejected() -> None:
    field = Field(10, 10)
    cars = [Car("A", Position(0, 0), Direction.N, "F")]
    new_cars, err = add_car(
        field, cars, "A", Position(1, 2), Direction.S, "RR"
    )
    assert new_cars is None
    assert "Duplicate" in (err or "")


def test_add_car_empty_name_rejected() -> None:
    field = Field(10, 10)
    cars: list[Car] = []
    new_cars, err = add_car(
        field, cars, "  ", Position(0, 0), Direction.N, "F"
    )
    assert new_cars is None
    assert err is not None


def test_run_simulation_returns_result() -> None:
    field = Field(10, 10)
    cars = [Car("A", Position(1, 2), Direction.N, "FF")]
    result = run_simulation(field, cars)
    assert not result.has_collision
    assert len(result.final_cars) == 1
    assert result.final_cars[0].position == Position(1, 4)


def test_run_simulation_collision() -> None:
    field = Field(10, 10)
    cars = [
        Car("A", Position(1, 2), Direction.N, "FFRFFFFRRL"),
        Car("B", Position(7, 8), Direction.W, "FFLFFFFFFF"),
    ]
    result = run_simulation(field, cars)
    assert result.has_collision
    assert len(result.collisions) == 2
