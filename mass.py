from periodic_table.periodic_table import element_from
from units import Mass_Unit, g
from utils.var_finder import get_missing_variables, triangle_equation
import utils.input_utils
import parse

class Mol:
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value} mol'

class Molar_Mass:
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value} g / mol'

def of_elements(element_list: list) -> Molar_Mass:
    '''
    element_list takes the form:

        [('He', 2)...]

    for 2 He atoms
    '''

    elements = [(element_from(name), value) for name, value in element_list]
    result = 0
    for element, value in elements:
        result += element['atomic_mass'] * value
    return Molar_Mass(result)

def of_molecule(molecule: str) -> Molar_Mass:
    return of_elements(
        parse.molecule_string(molecule)
    )

def of_molecule_from_input() -> Molar_Mass:
    return utils.input_utils.get(
        'please type a molecule (for example H20): ',
        of_molecule
    )

def missing_value() -> tuple:
    Mm, n, m = ['Mm', 'amount (mol)', 'mass (g)']

    known_variables = [(Mm, of_molecule_from_input().value)]
    input_variables = utils.input_utils.get_variables([m, n])

    if len(input_variables) != 1:
        raise ValueError('you must only input one variable')

    for input_variable in input_variables:
        known_variables.append(input_variable)

    equation = triangle_equation(Mm, n, m)
    missing = equation.get_missing_variable(known_variables)
    name, value = missing

    if name is m:
        return g(value)
    elif name is n:
        return Mol(value)

    raise ValueError('could not get the missing variable')