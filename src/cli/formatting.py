"""Format cars and simulation results for CLI output."""

from typing import List

from src.domain.car import Car
from src.service.simulation_engine import CollisionRecord, SimulationResult


def format_car_list(cars: List[Car]) -> str:
    """Format list of cars as '- A, (1,2) N, FFRFF' lines."""
    if not cars:
        return ""
    lines = [f"- {c.name}, ({c.position.x},{c.position.y}) {c.direction.value}, {c.commands}" for c in cars]
    return "\n".join(lines)


def format_simulation_result(result: SimulationResult, cars_before: List[Car]) -> str:
    """Format simulation result: either final positions or collision lines."""
    lines = ["After simulation, the result is:"]
    if result.has_collision:
        for rec in result.collisions:
            lines.append(f"- {rec.car_name}, collides with {rec.other_car_name} at ({rec.position.x},{rec.position.y}) at step {rec.step}")
    else:
        for car in result.final_cars:
            lines.append(f"- {car.name}, ({car.position.x},{car.position.y}) {car.direction.value}")
    return "\n".join(lines)
