from periodic_table.periodic_table import element_from
from units import Mass_Unit, g, mol_from_particles, particles_from_mol
from utils.var_finder import get_missing_variables, triangle_equation
import utils.input_utils
import parse

class Mol:
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value} mol'

    @property
    def particles(self) -> float:
        return particles_from_mol(self.value)

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

def missing_value():
    Mm, n, m, v, c = ['Mm', 'amount (mol)', 'mass (g)', 'volume (m^3)', 'consentration (g / m^3)']

    known_variables = [(Mm, of_molecule_from_input().value)]
    input_variables = utils.input_utils.get_variables([n, m, v, c])

    for input_variable in input_variables:
        known_variables.append(input_variable)

    equations = [
        triangle_equation(Mm, n, m),
        triangle_equation(c, v, m),
    ]
    result = get_missing_variables(known_variables, equations)

    print()
    for name, value in result:
        print(f'{name} = {value}')
    print()

    return result

def of_molecules(molecule: str, amount: float) -> float:
    mol = mol_from_particles(amount)
    return of_molecules_in_mol(molecule, mol)

def of_molecules_in_mol(molecule: str, mol: float) -> float:
    mass = of_molecule(molecule)
    return mass.value * mol