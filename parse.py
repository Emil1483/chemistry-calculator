import re

def molecule_string(name: str) -> list:
    '''
    takes a molecule string such as

        H2O

    and converts it to a list of tuples of the form

        [('H', 2), ('O', 1)]
    '''

    assert not name[0].isnumeric(), 'name cannot start with a number'
    assert name[0] == name[0].upper(), 'name must start with uppercase letter'

    regex = re.findall(r'[A-Z][a-z]*[0-9]*', name)
    length = 0
    for part in regex:
        length += len(part)
    
    assert length == len(name), f'{name} is badly formatted'

    result = []
    for part in regex:
        seperated = re.split(r'([A-Za-z]+)', part)
        seperated = [r for r in seperated if not r == '']
        if len(seperated) == 1:
            result.append((seperated[0], 1))
        else:
            elem, index = seperated
            result.append((elem, int(index)))

    return result