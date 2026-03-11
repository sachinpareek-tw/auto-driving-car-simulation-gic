"""Unit tests for CLI formatting."""

from src.domain.car import Car
from src.domain.position import Position
from src.domain.direction import Direction
from src.service.simulation_engine import SimulationResult, CollisionRecord
from src.cli.formatting import format_car_list, format_simulation_result


def test_format_car_list_empty() -> None:
    assert format_car_list([]) == ""


def test_format_car_list_one() -> None:
    cars = [Car("A", Position(1, 2), Direction.N, "FFRFF")]
    assert "A" in format_car_list(cars)
    assert "(1,2)" in format_car_list(cars)
    assert "N" in format_car_list(cars)
    assert "FFRFF" in format_car_list(cars)


def test_format_simulation_result_no_collision() -> None:
    cars = [Car("A", Position(5, 4), Direction.S, "")]
    result = SimulationResult(final_cars=cars)
    out = format_simulation_result(result, [])
    assert "After simulation" in out
    assert "A" in out
    assert "(5,4)" in out
    assert "S" in out


def test_format_simulation_result_collision() -> None:
    result = SimulationResult(
        collisions=[
            CollisionRecord("A", "B", Position(5, 4), 7),
            CollisionRecord("B", "A", Position(5, 4), 7),
        ],
        final_cars=[],
    )
    out = format_simulation_result(result, [])
    assert "collides with" in out
    assert "step 7" in out
