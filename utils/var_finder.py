from utils.input_utils import select_from_list, get_float
from utils.complex_utils import complex_round
import os


class Equation:
    '''
    An equation is used to find a missing variable if all other
    variables are known.
    A list of equations is used to find missing variables given
    a list of known variables.

    For example, to model the equation:
        v = v0 + a * t
    use:
        Equation([
            ('v', lambda v0, a, t: v0 + a * t),
            ('v0', lambda v, a, t: v - a * t),
            ('a', lambda v, v0, t: (v - v0) / t),
            ('t', lambda v, v0, a: (v - v0) / a),
        ])
    '''

    def __init__(self, variable_getters):
        self.variable_getters = variable_getters

    def index_of_variable_getter(self, variable_getters, variable_name):
        for i in range(len(variable_getters)):
            variable_getter_name = variable_getters[i][0]
            if variable_getter_name == variable_name:
                return i
        return -1

    def get_variable_from_name(self, variables, name):
        for variable in variables:
            if variable[0] == name:
                return variable[1]

    def get_missing_variable(self, variables):
        '''
        the variables take the form:

            [(name, value), ...]

        and it returns the missing

            (name, value)
        '''
        missing_variables_getters = self.variable_getters.copy()
        for variable in variables:
            index = self.index_of_variable_getter(
                missing_variables_getters,
                variable[0]
            )
            if index != -1:
                del missing_variables_getters[index]

        if len(missing_variables_getters) != 1:
            return None

        missing_variables_getter = missing_variables_getters[0]

        input_variable_names = [
            getter[0]
            for getter in self.variable_getters
            if getter[0] != missing_variables_getter[0]
        ]
        input_variables = []
        for name in input_variable_names:
            input_variables.append(
                self.get_variable_from_name(variables, name)
            )

        return (
            missing_variables_getter[0],
            missing_variables_getter[1](*input_variables)
        )


def triangle_equation(a: str, b: str, c: str) -> Equation:
    '''
    from an equation

        a = b * c

    this returns an Equation that can be used to find 
    the missing variable given two known variables
    '''
    return Equation([
        (c, lambda b, a: b * a),
        (b, lambda c, a: c / a),
        (a, lambda c, b: c / b),
    ])

def get_missing_variables(known_variables: list, equations: list) -> list:
    '''
    first paramater takes the form:

        [(name: string, value: float) ...]

    second paramater takes the form:

        [Equation() ...]
    '''
    result = [*known_variables]

    done = False
    while not done:
        done = True
        for equation in equations:
            missing = equation.get_missing_variable(result)
            if missing is not None:
                result.append(missing)
                done = False

    return result
