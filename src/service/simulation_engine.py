"""Simulation engine: runs steps (one command per car per step), bounds, collision."""

from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

from src.domain.car import Car, CMD_FORWARD, CMD_LEFT, CMD_RIGHT
from src.domain.field import Field
from src.domain.position import Position


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

        # Working copy: (car, is_stopped). is_stopped = already collided
        active: List[Tuple[Car, bool]] = [(c, False) for c in cars]
        collisions: List[CollisionRecord] = []
        step = 0  # 0-based

        while True:
            # Get command for each active car; if all done, break
            commands_this_step = []
            all_done = True
            for car, stopped in active:
                if stopped:
                    commands_this_step.append(None)
                    continue
                cmd = car.get_command_at_step(step)
                if cmd is not None:
                    all_done = False
                commands_this_step.append(cmd)

            if all_done:
                break

            # Compute proposed next state for each car (position and/or direction)
            proposed: List[Optional[Tuple[Position, Optional[Car]]]] = []
            for i, ((car, stopped), cmd) in enumerate(zip(active, commands_this_step)):
                if stopped:
                    proposed.append((car.position, None))  # no change
                    continue
                if cmd is None:
                    proposed.append((car.position, None))
                    continue
                if cmd == CMD_LEFT:
                    proposed.append((car.position, car.with_rotation_left()))
                    continue
                if cmd == CMD_RIGHT:
                    proposed.append((car.position, car.with_rotation_right()))
                    continue
                # cmd == CMD_FORWARD
                next_pos = car.position_after_forward()
                if field.is_within_bounds(next_pos):
                    proposed.append((next_pos, car.with_position(next_pos)))
                else:
                    proposed.append((car.position, None))  # stay

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
                        if not active[idx][1]:  # not already stopped
                            collided_this_step.add(idx)

            step_1based = step + 1
            if collided_this_step:
                # One record per collided car: "A collides with B at (x,y) at step N"
                collided_list = sorted(collided_this_step)
                for idx, i in enumerate(collided_list):
                    j = collided_list[(idx + 1) % len(collided_list)]  # another collided car
                    car_i = active[i][0]
                    car_j = active[j][0]
                    pos = Position(proposed[i][0].x, proposed[i][0].y)
                    collisions.append(
                        CollisionRecord(
                            car_name=car_i.name,
                            other_car_name=car_j.name,
                            position=pos,
                            step=step_1based,
                        )
                    )
                # Mark these cars as stopped (keep current position, don't apply move)
                new_active: List[Tuple[Car, bool]] = []
                for i, (car, stopped) in enumerate(active):
                    if i in collided_this_step:
                        new_active.append((car, True))  # stopped at current position
                    else:
                        pos, updated = proposed[i]
                        if updated is not None:
                            new_active.append((updated, stopped))
                        else:
                            new_active.append((car, stopped))
                active = new_active
            else:
                # Apply proposed updates
                new_active = []
                for i, (car, stopped) in enumerate(active):
                    _, updated = proposed[i]
                    if updated is not None:
                        new_active.append((updated, stopped))
                    else:
                        new_active.append((car, stopped))
                active = new_active

            step += 1

        if collisions:
            # Return collision result: final cars are the state when they collided
            final_cars = [car for car, _ in active]
            return SimulationResult(collisions=collisions, final_cars=final_cars)
        return SimulationResult(final_cars=[car for car, _ in active])
