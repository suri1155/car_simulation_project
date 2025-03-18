from car_simulation.car import CarStorage, Car
from car_simulation.cli import run_simulator, start_simulator


class TestSimulation:
    def test_cars_start_with_single_car(self):
        _car = Car("car1", (3, 3), "N", "FF" )
        car_db = CarStorage()
        car_db.add_car(_car)
        x_axis, y_axis = 10, 10
        all_cars_data = {'car1': {'car_name': 'car1', 'initial_coordinates': (3, 3), 'execute_cmd': 'FF',
                                  'car_direction': 'N'}}
        start_simulator(all_cars_data, x_axis, y_axis, car_db)

    def test_cars_start_with_same_origin_and_never_collide(self):
        x_axis, y_axis = 10, 10
        all_cars_data = {'car1': {'car_name': 'car1', 'initial_coordinates': (3, 3), 'execute_cmd': 'FF',
                                  'car_direction': 'N'},
                         'car2': {'car_name': 'car2', 'initial_coordinates': (3, 3), 'execute_cmd': 'FF',
                                  'car_direction': 'S'}}
        simulator_result = run_simulator(all_cars_data, x_axis, y_axis)

        assert simulator_result == {
            'car1': {'car_name': 'car1', 'initial_coordinates': (3, 3), 'execute_cmd': 'FF', 'car_direction': 'N',
                     'current_direction': 'N', 'curr_coordinates': (3, 5), 'final_direction': 'N'
                , 'final_coordinates': (3, 5)},
            'car2': {'car_name': 'car2', 'initial_coordinates': (3, 3), 'execute_cmd': 'FF', 'car_direction': 'S',
                     'current_direction': 'S', 'curr_coordinates': (3, 1), 'final_direction': 'S',
                     'final_coordinates': (3, 1)}}

    def test_cars_start_with_diff_origin_and_collide(self):
        x_axis, y_axis = 10, 10
        all_cars_data = {'car1': {'car_name': 'car1', 'initial_coordinates': (8, 8), 'execute_cmd': 'FF',
                                  'car_direction': 'N'},
                         'car2': {'car_name': 'car2', 'initial_coordinates': (9, 9), 'execute_cmd': 'FF',
                                  'car_direction': 'W'}}
        simulator_result = run_simulator(all_cars_data, x_axis, y_axis)

        assert simulator_result == {
            'car1': {'car_name': 'car1', 'initial_coordinates': (8, 8), 'execute_cmd': 'FF', 'car_direction': 'N',
                     'current_direction': 'N', 'curr_coordinates': (8, 9), 'stopped_at': 1, 'collide_with': ['car2'],
                     'collide_coordinates': (8, 9)},
            'car2': {'car_name': 'car2', 'initial_coordinates': (9, 9), 'execute_cmd': 'FF', 'car_direction': 'W',
                     'current_direction': 'W', 'curr_coordinates': (8, 9), 'stopped_at': 1, 'collide_with': ['car1'],
                     'collide_coordinates': (8, 9)}}

    def test_with_some_cars_collide_and_some_does_not_collide(self):
        x_axis, y_axis = 10, 10
        all_cars_data = {
            'car1': {'car_name': 'car1', 'initial_coordinates': (8, 8), 'execute_cmd': 'FF',
                     'car_direction': 'N'},
            'car2': {'car_name': 'car2', 'initial_coordinates': (9, 9), 'execute_cmd': 'FF',
                     'car_direction': 'W'},
            'car3': {'car_name': 'car3', 'initial_coordinates': (1, 2), 'execute_cmd': 'FFRFFFFRRL',
                     'car_direction':
                         'N'},
            'car4': {'car_name': 'car4', 'initial_coordinates': (1, 7), 'execute_cmd': 'FFRFFR',
                     'car_direction':
                         'N'}
        }
        simulator_result = run_simulator(all_cars_data, x_axis, y_axis)

        assert simulator_result == {
            'car1': {'car_name': 'car1', 'initial_coordinates': (8, 8), 'execute_cmd': 'FF', 'car_direction': 'N',
                     'current_direction': 'N', 'curr_coordinates': (8, 9),
                     'stopped_at': 1, 'collide_with': ['car2'], 'collide_coordinates': (8, 9)},
            'car2': {'car_name': 'car2', 'initial_coordinates': (9, 9), 'execute_cmd': 'FF', 'car_direction': 'W',
                     'current_direction': 'W', 'curr_coordinates': (8, 9), 'stopped_at': 1, 'collide_with': ['car1'],
                     'collide_coordinates': (8, 9)}, 'car3': {'car_name': 'car3', 'initial_coordinates': (
                1, 2), 'execute_cmd': 'FFRFFFFRRL', 'car_direction': 'N', 'current_direction': 'S',
                                                              'curr_coordinates': (5, 4), 'final_direction': 'S',
                                                              'final_coordinates': (5, 4)},
            'car4': {'car_name': 'car4', 'initial_coordinates': (1, 7), 'execute_cmd': 'FFRFFR', 'car_direction': 'N',
                     'current_direction': 'S', 'curr_coordinates': (3, 9), 'final_direction': 'S',
                     'final_coordinates': (3, 9)}}

    def test_car_tries_go_out_simulation(self):
        x_axis, y_axis = 3, 3
        all_cars_data = {'car1': {'car_name': 'car1', 'initial_coordinates': (2, 2), 'execute_cmd': 'FFFFFF',
                                  'car_direction': 'N'}}
        simulator_result = run_simulator(all_cars_data, x_axis, y_axis)

        assert simulator_result == {
            'car1': {'car_name': 'car1', 'initial_coordinates': (2, 2), 'execute_cmd': 'FFFFFF', 'car_direction': 'N',
                     'current_direction': 'N', 'curr_coordinates': (2, 3), 'final_direction': 'N',
                     'final_coordinates': (2, 3)}}
