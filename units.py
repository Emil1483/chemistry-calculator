class Mass_Unit:
    def __init__(self, rate: float, value: float):
        self.rate = rate
        self.value = value

    @property
    def in_g(self) -> float:
        return self.value * self.rate

    def __str__(self):
        return f'{self.value} {type(self).__name__}'

class Kg(Mass_Unit):
    def __init__(self, value: float):
        super().__init__(1e3, value)

class g(Mass_Unit):
    def __init__(self, value: float):
        super().__init__(1, value)

class mg(Mass_Unit):
    def __init__(self, value: float):
        super().__init__(1e-3, value)