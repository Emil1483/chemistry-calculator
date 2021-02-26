import json

def element_from(name: str) -> float:
    with open('periodic_table/table.json') as f:
        elements = json.load(f)['elements']
        for element in elements:
            if element['name'].lower() == name.lower():
                return element
            if element['symbol'].lower() == name.lower():
                return element
        
    raise ValueError(f'element \'{name}\' does not exist')