"""Unit tests for SimulationEngine."""

import pytest
from src.domain.car import Car
from src.domain.field import Field
from src.domain.position import Position
from src.domain.direction import Direction
from src.service.simulation_engine import SimulationEngine, SimulationResult


def test_single_car_no_collision() -> None:
    """Scenario 1: one car, run commands, get final position."""
    field = Field(10, 10)
    car = Car("A", Position(1, 2), Direction.N, "FFRFFFFRRL")
    engine = SimulationEngine()
    result = engine.run(field, [car])
    assert not result.has_collision
    assert len(result.final_cars) == 1
    assert result.final_cars[0].name == "A"
    assert result.final_cars[0].position == Position(5, 4)
    assert result.final_cars[0].direction == Direction.S


def test_single_car_boundary_ignore() -> None:
    """F at boundary is ignored; car stays."""
    field = Field(3, 3)
    car = Car("A", Position(0, 0), Direction.S, "F")  # would go to (0,-1)
    engine = SimulationEngine()
    result = engine.run(field, [car])
    assert not result.has_collision
    assert result.final_cars[0].position == Position(0, 0)


def test_two_cars_no_collision() -> None:
    """Two cars, no collision; both reach final positions."""
    field = Field(10, 10)
    car_a = Car("A", Position(0, 0), Direction.N, "F")
    car_b = Car("B", Position(9, 9), Direction.S, "F")
    engine = SimulationEngine()
    result = engine.run(field, [car_a, car_b])
    assert not result.has_collision
    assert len(result.final_cars) == 2
    by_name = {c.name: c for c in result.final_cars}
    assert by_name["A"].position == Position(0, 1)
    assert by_name["B"].position == Position(9, 8)


def test_two_cars_collision() -> None:
    """Two cars collide; result has collision records and step number."""
    # From README: A (1,2) N FFRFFFFRRL, B (7,8) W FFLFFFFFFF -> collide at (5,4) at step 7
    field = Field(10, 10)
    car_a = Car("A", Position(1, 2), Direction.N, "FFRFFFFRRL")
    car_b = Car("B", Position(7, 8), Direction.W, "FFLFFFFFFF")
    engine = SimulationEngine()
    result = engine.run(field, [car_a, car_b])
    assert result.has_collision
    assert len(result.collisions) == 2  # A with B, B with A
    steps = {r.step for r in result.collisions}
    assert steps == {7}
    positions = {r.position for r in result.collisions}
    assert positions == {Position(5, 4)}
    names = {r.car_name for r in result.collisions}
    assert names == {"A", "B"}


def test_different_command_lengths_car_stays_put() -> None:
    """When one car runs out of commands, it stays put while other continues."""
    field = Field(10, 10)
    car_a = Car("A", Position(0, 0), Direction.N, "F")  # one step
    car_b = Car("B", Position(2, 0), Direction.N, "FFF")  # three steps
    engine = SimulationEngine()
    result = engine.run(field, [car_a, car_b])
    assert not result.has_collision
    by_name = {c.name: c for c in result.final_cars}
    assert by_name["A"].position == Position(0, 1)
    assert by_name["B"].position == Position(2, 3)


def test_empty_cars() -> None:
    engine = SimulationEngine()
    result = engine.run(Field(10, 10), [])
    assert not result.has_collision
    assert result.final_cars == []


def test_single_car_no_commands() -> None:
    field = Field(10, 10)
    car = Car("A", Position(1, 2), Direction.N, "")
    engine = SimulationEngine()
    result = engine.run(field, [car])
    assert not result.has_collision
    assert result.final_cars[0].position == Position(1, 2)
