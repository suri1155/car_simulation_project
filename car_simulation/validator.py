import re

from pydantic import BaseModel, field_validator, model_validator

class CustomException(Exception):
    def __init__(self, description=None):
        self.description = description


class SimulatorInputValues(BaseModel):
    x: int
    y: int


    # Field validator for car_x and car_y to check if the values are non-negative
    @field_validator('x', 'y')
    def check_non_negative(cls, value):
        if value < 0:
            raise CustomException(f"{value} must be a non-negative number")
        return value

    # Model validator to check that car_x and car_y are not both zero
    @model_validator(mode="before")
    def check_not_both_zero(cls, values):
        # Check if both car_x and car_y are zero
        if values.get('x') == 0 and values.get('y') == 0:
            raise CustomException("Sorry, simulation cannot be performed with (0, 0). Please enter other values.")
        return values



class CarInputValues(BaseModel):
    x: int
    y: int
    x_axis: int
    y_axis: int

    @model_validator(mode="before")
    def check_not_both_zero(cls, values):

        if not (0 <= values.get('x') <= values.get('x_axis')):
            raise CustomException(f"x is out of bounds. It must be between 0 and {values.get('x_axis')}.")
        elif not (0 <= values.get('y') <= values.get('y_axis')):
            raise CustomException(f"y is out of bounds. It must be between 0 and {values.get('y_axis')}.")
        return values


def validate_simulation_coordinates(x_axis, y_axis):
    flag = True
    try:
        SimulatorInputValues(x=x_axis, y=y_axis)
    except Exception as e:
        print(e)
        flag = False
    return flag

def validate_car_coordinates(car_x, car_y, x_axis, y_axis):
    flag = True
    try:
        CarInputValues(x=car_x, y=car_y, x_axis=x_axis, y_axis=y_axis)
    except Exception as e:
        print(e)
        flag = False
    return flag

def validate_car_direction(direction):
    result =  False if direction not in ['N', 'S', 'E', 'W'] else True
    return result

def validate_clean_execute_cmd(car_commands:str):
    return re.sub(r"[^FRL]", "", car_commands.upper())


def check_car_pos_and_dir(car_pos_and_dir, x_axis, y_axis):
    result = []

    input_list = car_pos_and_dir.split()
    if len(input_list) == 3:
        car_x, car_y, direction = input_list
        coordinate_flag = validate_car_coordinates(int(car_x), int(car_y), x_axis, y_axis)
        direction_flag = validate_car_direction(direction.upper())

        if coordinate_flag and direction_flag:
            result = input_list

    return result
