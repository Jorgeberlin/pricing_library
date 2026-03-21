from dataclasses import dataclass

@dataclass (slots=True)
class BinomialModel:
    spot: float
    rate: float
    up: float
    down: float