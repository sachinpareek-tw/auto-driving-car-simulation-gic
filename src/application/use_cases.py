"""Application / use-case layer: Add car, Run simulation, Start over."""

from typing import List, Optional, Tuple

from src.domain.car import Car
from src.domain.direction import Direction
from src.domain.field import Field
from src.domain.position import Position
from src.service.simulation_engine import SimulationEngine, SimulationResult


def create_field(width: int, height: int) -> Field:
    """Create a field with given dimensions. Raises ValueError if invalid."""
    return Field(width=width, height=height)


def add_car(
    field: Field,
    cars: List[Car],
    name: str,
    position: Position,
    direction: Direction,
    commands: str,
) -> Tuple[Optional[List[Car]], Optional[str]]:
    """
    Add a car to the simulation. Returns (new_cars_list, None) on success,
    or (None, error_message) on duplicate name.
    """
    name_clean = name.strip()
    if not name_clean:
        return None, "Car name cannot be empty"
    for c in cars:
        if c.name == name_clean:
            return None, f"Duplicate car name: {name_clean}"
    car = Car(name=name_clean, position=position, direction=direction, commands=commands)
    return cars + [car], None


def run_simulation(field: Field, cars: List[Car]) -> SimulationResult:
    """Run the simulation for all cars. Returns final positions or collision records."""
    engine = SimulationEngine()
    return engine.run(field, cars)
