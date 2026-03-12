"""CLI main loop: prompts, menus, and wiring to use cases."""

from typing import Callable, List, Optional

from src.domain.car import Car
from src.domain.field import Field
from src.application.use_cases import create_field, add_car, run_simulation
from src.cli.parser import parse_field_dimensions, parse_position_direction, parse_commands
from src.cli.formatting import format_car_list, format_simulation_result


def run(
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> None:
    """Run the CLI simulation. Uses input_func for reading, print_func for output."""
    print_func("Welcome to Auto Driving Car Simulation!")
    print_func("")
    field: Optional[Field] = None
    cars: List[Car] = []
    post_simulation: bool = False

    while True:
        if field is None:
            print_func("Please enter the width and height of the simulation field in x y format:")
            line = input_func("").strip()
            dims = parse_field_dimensions(line)
            if dims is None:
                print_func("Invalid dimensions. Please enter two positive integers (e.g. 10 10).")
                continue
            width, height = dims
            try:
                field = create_field(width, height)
            except ValueError as e:
                print_func(str(e))
                continue
            print_func(f"You have created a field of {width} x {height}.")
            print_func("")

        if post_simulation:
            print_func("Please choose from the following options:")
            print_func("[1] Start over")
            print_func("[2] Exit")
            print_func("")
            choice = input_func("").strip()
            if choice == "1":
                field = None
                cars = []
                post_simulation = False
                print_func("Welcome to Auto Driving Car Simulation!")
                print_func("")
                continue
            if choice == "2":
                print_func("Thank you for running the simulation. Goodbye!")
                return
            print_func("Invalid option. Please enter 1 or 2.")
            continue

        # Main menu: Add car / Run simulation
        print_func("Please choose from the following options:")
        print_func("[1] Add a car to field")
        print_func("[2] Run simulation")
        print_func("")
        choice = input_func("").strip()
        if choice == "1":
            _do_add_car(field, cars, input_func, print_func)
            continue
        if choice == "2":
            if not cars:
                print_func("Add at least one car before running simulation.")
                continue
            _do_run_simulation(field, cars, print_func)
            post_simulation = True
            continue
        print_func("Invalid option. Please enter 1 or 2.")


def _do_add_car(
    field: Field,
    cars: List[Car],
    input_func: Callable[[str], str],
    print_func: Callable[[str], None],
) -> None:
    print_func("Please enter the name of the car:")
    name = input_func("").strip()
    print_func(f"Please enter initial position of car {name} in x y Direction format:")
    pos_line = input_func("").strip()
    parsed = parse_position_direction(pos_line)
    if parsed is None:
        print_func("Only N, S, W, E (representing North, South, West, East) are allowed for direction.")
        return
    position, direction = parsed
    print_func(f"Please enter the commands for car {name}:")
    commands = parse_commands(input_func(""))
    new_cars, err = add_car(field, cars, name, position, direction, commands)
    if err:
        print_func(err)
        return
    cars.clear()
    cars.extend(new_cars or [])
    print_func("Your current list of cars are:")
    print_func(format_car_list(cars))
    print_func("")


def _do_run_simulation(field: Field, cars: List[Car], print_func: Callable[[str], None]) -> None:
    print_func("Your current list of cars are:")
    print_func(format_car_list(cars))
    print_func("")
    result = run_simulation(field, cars)
    print_func(format_simulation_result(result, cars))
    print_func("")


def main() -> None:
    """Entry point when run as module or script."""
    run()


if __name__ == "__main__":
    main()
