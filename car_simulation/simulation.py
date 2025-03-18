from collections import defaultdict

directions = {
    "N": {
        "L": "W",
        "R": "E"
    },
    "E": {
        "L": "N",
        "R": "S"
    },
    "S": {
        "L": "E",
        "R": "W"
    },
    "W": {
        "L": "S",
        "R": "N"
    }
}


def move_coordinates(direction, x, y, x_axis, y_axis):
    if direction == "N" and 0<= y < y_axis:
        y += 1
    elif direction == "S" and 0 < y < y_axis:
        y -= 1
    elif direction == "E" and 0 < x < x_axis:
        x += 1
    elif direction == "W" and 0 < x < x_axis:
        x -= 1
    return x, y

def simulate_movement(current_direction, start_x, start_y, action, x_axis, y_axis):

    x, y = start_x, start_y

    if action == "F":
        x, y = move_coordinates(current_direction, x, y, x_axis, y_axis)

    else:
        current_direction = directions[current_direction][action]

    return current_direction, (x, y)


def check_for_collision(car_data, step, stopped_cars):
    car_data = {key: value for key, value in car_data.items() if key not in stopped_cars}
    coord_groups = defaultdict(list)

    # Group cars by coordinates
    for car, details in car_data.items():
        coord_groups[details["curr_coordinates"]].append(car)

    # Filter only those coordinates where multiple cars exist
    cars_at_same_location = {coord: cars for coord, cars in coord_groups.items() if len(cars) > 1}

    #update db data
    for coordinates, cars in cars_at_same_location.items():
        stopped_cars.extend(cars)
        for car in cars:
            car_data[car]["stopped_at"] = step + 1

            if "collide_with" in car_data[car]:
                car_data[car]["collide_with"].extend(list(set(cars) - {car}))
            else:
                car_data[car]["collide_with"] = list(set(cars) - {car})

            car_data[car]["collide_coordinates"] = coordinates
            car_data[car]["collide_with"] = list(set(car_data[car]["collide_with"]))
    return car_data, stopped_cars

def run_simulator(all_cars_data, x_axis, y_axis):
    simulated_car_data = {}

    max_steps = max(len(data['execute_cmd']) for data in all_cars_data.values())

    stopped_cars = []
    for step in range(0, max_steps+1):
        # Move each car one step and check for collisions
        for car_name, car_info in all_cars_data.items():

            if car_name not in stopped_cars:
                if step == len(car_info["execute_cmd"]):
                    car_info["final_direction"], car_info["final_coordinates"] = car_info["current_direction"], \
                        car_info["curr_coordinates"]
                    stopped_cars.append(car_name)

                else:
                    x, y = car_info.get("curr_coordinates", car_info["initial_coordinates"])
                    _current_direction = car_info.get("current_direction", car_info["car_direction"])

                    car_info["current_direction"], car_info["curr_coordinates"] = simulate_movement(
                        _current_direction, x, y,
                        car_info["execute_cmd"][step],
                        x_axis, y_axis)
                all_cars_data[car_name] = car_info

        collided_cars_data, stopped_cars = check_for_collision(all_cars_data, step, stopped_cars)
        simulated_car_data.update(collided_cars_data)

    return simulated_car_data
