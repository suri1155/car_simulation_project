import traceback

from car_simulation.car import CarStorage, Car
from car_simulation.simulation import run_simulator
from car_simulation.validator import validate_simulation_coordinates, validate_clean_execute_cmd, check_car_pos_and_dir


def get_user_inputs():
    print("Welcome to Auto Driving Car Simulation!", end="\n")
    print("Please enter the width and height of the simulation field in x y format:", end="\n")
    try:
        x_axis, y_axis = input().split()
        x_axis, y_axis = int(x_axis), int(y_axis)

        validate_simulation_coordinates(x_axis=x_axis, y_axis=y_axis)

        print(f"You have created a field of {x_axis} * {y_axis}", end="\n")
        car_db = CarStorage()
        while True:

            print("\nPlease choose from the following options:")
            print("[1] Add a car to field")
            print("[2] Run simulation", end="\n")
            choice = input()

            if choice == "1":
                add_cars(car_db, x_axis, y_axis)
            elif choice == "2":
                all_cars_data = car_db.get_all_car_info()

                start_simulator(all_cars_data, x_axis, y_axis, car_db)

                break
            else:
                print("Invalid option. Please choose either [1], [2]")

    except ValueError:
        print("Invalid input, Please enter valid input again.")
    except Exception as e:
        print(traceback.format_exc())
        print(f"Error: {e}")

def add_cars(car_db, x_axis, y_axis):
    car_name = input("\nPlease enter the name of the car:\n")

    car_pos_and_dir = input(
        f"\nPlease enter initial position of car {car_name} in x y Direction format:\n")

    _car_pos_and_dir = check_car_pos_and_dir(car_pos_and_dir=car_pos_and_dir, x_axis=x_axis,
                                             y_axis=y_axis)

    while not _car_pos_and_dir:
        car_pos_and_dir = input("\nInvalid input, Please reenter initial position of "
                                f"car {car_name} in x y Direction format:\n")
        _car_pos_and_dir = check_car_pos_and_dir(car_pos_and_dir=car_pos_and_dir, x_axis=x_axis,
                                                 y_axis=y_axis)

    car_x, car_y, direction = _car_pos_and_dir
    car_x, car_y, direction = int(car_x), int(car_y), direction.upper()

    commands = input(f"\nPlease enter the commands for car {car_name}:\n")
    commands = validate_clean_execute_cmd(commands)
    while not commands:
        commands = input(f"\nInvalid commands,Please reenter the commands for car {car_name}:\n")
        commands = validate_clean_execute_cmd(commands)

    new_car = Car(car_name, (car_x, car_y), direction, commands)

    car_db.add_car(new_car)

    print("Your current list of cars are:", end="\n")
    car_db.display_all_cars_info()


def start_simulator(all_cars_data, x_axis, y_axis, car_db):
    simulated_car_data = run_simulator(all_cars_data, x_axis, y_axis)

    print("Your current list of cars are:", end="\n")
    car_db.display_all_cars_info()

    print("\nAfter simulation, the result is:", end="\n")
    for car_name, car_info in simulated_car_data.items():
        if car_info.get("stopped_at", None) is not None:
            print(f"- {car_name}, collides with "
                  f"{', '.join(car_info['collide_with'])} at {car_info['collide_coordinates']} at step"
                  f" {car_info['stopped_at']}", end="\n")
        else:
            print(f'- {car_info["car_name"]}, {car_info["final_coordinates"]}'
                  f' {car_info["final_direction"]} '
                  , end="\n")