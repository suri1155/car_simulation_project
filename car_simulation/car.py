class Car:
    def __init__(self, car_name: str, initial_coordinates: tuple, car_direction: str, execute_cmd: str):
        self.car_name = car_name
        self.initial_coordinates = initial_coordinates
        self.execute_cmd = execute_cmd
        self.car_direction = car_direction


class CarStorage:
    def __init__(self):
        self.cars_data = {}

    def add_car(self, car: Car):
        self.cars_data[car.car_name] = car.__dict__

    def display_all_cars_info(self):
        """Displays the current status of all cars."""
        for _, car in self.cars_data.items():
            print(f'- {car["car_name"]}, {car["initial_coordinates"]} {car["car_direction"]}, '
                  f'{car["execute_cmd"]}', end="\n")

    def get_all_car_info(self):
        return self.cars_data
