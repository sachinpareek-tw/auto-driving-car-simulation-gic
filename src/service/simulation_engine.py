"""Simulation engine: runs steps (one command per car per step), bounds, collision."""

from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

from src.domain.car import Car
from src.domain.field import Field
from src.domain.position import Position


@dataclass
class CarState:
    """Per-car simulation state: the car and whether it has stopped (e.g. after collision)."""

    car: Car
    stopped: bool


@dataclass
class CollisionRecord:
    """One car's view of a collision: name, other car name, position, step (1-based)."""

    car_name: str
    other_car_name: str
    position: Position
    step: int  # 1-based for display


@dataclass
class SimulationResult:
    """Result of running simulation: either final positions or collision records."""

    collisions: List[CollisionRecord] = field(default_factory=list)
    final_cars: List[Car] = field(default_factory=list)

    @property
    def has_collision(self) -> bool:
        return len(self.collisions) > 0


class SimulationEngine:
    """Runs simulation: one command per car per step, boundary check, collision detection."""

    def run(self, field: Field, cars: List[Car]) -> SimulationResult:
        """
        Run all steps until no car has more commands or a collision occurs.
        Returns final positions for all cars, or collision records if any collision.
        """
        if not cars:
            return SimulationResult(final_cars=[])

        # Working copy: car + stopped flag (stopped = already collided)
        active: List[CarState] = [CarState(car=c, stopped=False) for c in cars]
        collisions: List[CollisionRecord] = []
        step = 0  # 0-based

        while True:
            # Get command for each active car; if all done, break
            commands_this_step = []
            all_done = True
            for state in active:
                if state.stopped:
                    commands_this_step.append(None)
                    continue
                cmd = state.car.get_command_at_step(step)
                if cmd is not None:
                    all_done = False
                commands_this_step.append(cmd)

            if all_done:
                break

            # Compute proposed next state for each car (domain executes command)
            proposed: List[Optional[Tuple[Position, Optional[Car]]]] = []
            for state, cmd in zip(active, commands_this_step):
                if state.stopped:
                    proposed.append((state.car.position, None))
                    continue
                result = state.car.execute_command(cmd, field)
                proposed.append((result.position, result.updated_car))

            # Collision check: which positions are occupied (by car index)
            position_to_indices: dict[Tuple[int, int], List[int]] = {}
            for i, (pos, _) in enumerate(proposed):
                key = (pos.x, pos.y)
                if key not in position_to_indices:
                    position_to_indices[key] = []
                position_to_indices[key].append(i)

            collided_this_step: Set[int] = set()
            for indices in position_to_indices.values():
                if len(indices) >= 2:
                    for idx in indices:
                        if not active[idx].stopped:
                            collided_this_step.add(idx)

            step_1based = step + 1
            if collided_this_step:
                # One record per collided car: "A collides with B at (x,y) at step N"
                collided_list = sorted(collided_this_step)
                for idx, i in enumerate(collided_list):
                    j = collided_list[(idx + 1) % len(collided_list)]  # another collided car
                    car_i = active[i].car
                    car_j = active[j].car
                    pos = Position(proposed[i][0].x, proposed[i][0].y)
                    collisions.append(
                        CollisionRecord(
                            car_name=car_i.name,
                            other_car_name=car_j.name,
                            position=pos,
                            step=step_1based,
                        )
                    )

            # Apply proposed updates or mark collided cars as stopped (single loop)
            new_active = []
            for i, state in enumerate(active):
                if i in collided_this_step:
                    new_active.append(CarState(car=state.car, stopped=True))
                else:
                    _, updated = proposed[i]
                    new_active.append(
                        CarState(
                            car=updated if updated is not None else state.car,
                            stopped=state.stopped,
                        )
                    )
            active = new_active

            step += 1

        if collisions:
            # Return collision result: final cars are the state when they collided
            final_cars = [s.car for s in active]
            return SimulationResult(collisions=collisions, final_cars=final_cars)
        return SimulationResult(final_cars=[s.car for s in active])
