"""Integration tests: full simulation scenarios with expected formatted output."""

from src.domain.car import Car
from src.domain.direction import Direction
from src.domain.field import Field
from src.domain.position import Position
from src.application.use_cases import run_simulation
from src.cli.formatting import format_simulation_result


def test_simulation_1_three_cars_final_positions() -> None:
    """Simulation 1: C, B, A on 10x10; expect C (4,6) W, B (0,0) W, A (1,0) E."""
    field = Field(10, 10)
    cars = [
        Car("C", Position(3, 5), Direction.N, "FRFFFRRFF"),
        Car("B", Position(1, 0), Direction.W, "F"),
        Car("A", Position(0, 0), Direction.E, "F"),
    ]
    result = run_simulation(field, cars)
    out = format_simulation_result(result, cars)
    assert not result.has_collision
    assert "- C, (4,6) W" in out
    assert "- B, (0,0) W" in out
    assert "- A, (1,0) E" in out


def test_simulation_2_two_cars_final_positions() -> None:
    """Simulation 2: B, A on 10x10; expect B (0,1) S, A (9,4) E."""
    field = Field(10, 10)
    cars = [
        Car("B", Position(3, 8), Direction.W, "FFFFFFLFFFFFFF"),
        Car("A", Position(3, 4), Direction.E, "FFFFFFFFF"),
    ]
    result = run_simulation(field, cars)
    out = format_simulation_result(result, cars)
    assert not result.has_collision
    assert "- B, (0,1) S" in out
    assert "- A, (9,4) E" in out


def test_simulation_3_collision_at_step_2() -> None:
    """Simulation 3: D and K collide at (3,2) at step 2."""
    field = Field(10, 10)
    cars = [
        Car("D", Position(1, 2), Direction.E, "FF"),
        Car("K", Position(3, 4), Direction.S, "FF"),
    ]
    result = run_simulation(field, cars)
    out = format_simulation_result(result, cars)
    assert result.has_collision
    assert "- D, collides with K at (3,2) at step 2" in out
    assert "- K, collides with D at (3,2) at step 2" in out


def test_spec_example_single_car_a_final_position() -> None:
    """Spec example Scenario 1: Car A (1,2) N FFRFFFFRRL → (5,4) S."""
    field = Field(10, 10)
    cars = [Car("A", Position(1, 2), Direction.N, "FFRFFFFRRL")]
    result = run_simulation(field, cars)
    out = format_simulation_result(result, cars)
    assert not result.has_collision
    assert "- A, (5,4) S" in out


def test_spec_example_two_cars_collision_at_step_7() -> None:
    """Spec example Scenario 2: A (1,2) N FFRFFFFRRL, B (7,8) W FFLFFFFFFF → collision at (5,4) at step 7."""
    field = Field(10, 10)
    cars = [
        Car("A", Position(1, 2), Direction.N, "FFRFFFFRRL"),
        Car("B", Position(7, 8), Direction.W, "FFLFFFFFFF"),
    ]
    result = run_simulation(field, cars)
    out = format_simulation_result(result, cars)
    assert result.has_collision
    assert "- A, collides with B at (5,4) at step 7" in out
    assert "- B, collides with A at (5,4) at step 7" in out
