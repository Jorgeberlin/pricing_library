from dataclasses import dataclass

@dataclass (slots=True)
class AsianOption:
    maturity:int
    strike:float
    is_call:bool

