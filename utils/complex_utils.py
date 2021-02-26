def complex_round(num, rounding):
    if type(num) is complex:
        return round(num.real, rounding) + round(num.imag, rounding) * 1j
    
    return round(num, rounding)