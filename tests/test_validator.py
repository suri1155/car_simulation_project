import pytest

from car_simulation.validator import validate_simulation_coordinates, validate_car_coordinates, validate_car_direction, \
    check_car_pos_and_dir, validate_clean_execute_cmd


class TestSimulationCoordinates:
    @pytest.mark.parametrize("x_axis, y_axis, result", [(0, 1, True), (1,0,True),
                                                        (1,1,True),(10,10,True),
                                                        (0,0,False), (-1,0, False)])
    # @pytest.mark.parametrize("x_axis, y_axis, result", [(0, 1, True)])
    def test_simulation_with_coordinates_0_n_or_n_0(self, x_axis, y_axis, result):
        validated_result = validate_simulation_coordinates(x_axis=x_axis, y_axis=y_axis)
        assert result == validated_result

class TestCarValidation:
    @pytest.mark.parametrize("car_x, car_y, x_axis, y_axis, result", [(0, 1, 2, 2, True), (3,3,2,2, False),
                                                        (1,3,2,2, False), (0,0,0,0, True)])
    # @pytest.mark.parametrize("x_axis, y_axis, result", [(0, 1, True)])
    def test_car_initial_coordinates(self, car_x, car_y, x_axis, y_axis, result):
        validated_result = validate_car_coordinates(car_x, car_y, x_axis, y_axis)
        assert result == validated_result

    @pytest.mark.parametrize("direction, result", [("N", True), ("S", True), ("E", True), ("W", True), ("Q", False)])
    def test_validate_car_direction(self, direction, result):
        validated_result = validate_car_direction(direction)
        assert result == validated_result

    @pytest.mark.parametrize("car_inputs, x_axis, y_axis, result", [("1 2 N", 3, 3,  ['1', '2', 'N']),
                                                                    ("1 2 J", 3, 3, [])])
    def test_check_car_pos_and_dir(self, car_inputs, x_axis, y_axis, result):
        validated_result = check_car_pos_and_dir(car_inputs, x_axis, y_axis)
        assert result == validated_result

    @pytest.mark.parametrize("execute_cmd, result", [("FTTFRGFF", "FFRFF")])
    def test_validate_execute_cmd(self, execute_cmd, result):
        validated_result = validate_clean_execute_cmd(execute_cmd)
        assert result == validated_result