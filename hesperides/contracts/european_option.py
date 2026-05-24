from dataclasses import dataclass

@dataclass (slots=True)
class EuropeanOption:
    maturity:int
    strike:float
    is_call:bool
