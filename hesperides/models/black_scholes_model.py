from dataclasses import dataclass

@dataclass (slots=True)
class BlackScholesModel:
    spot: float
    rate: float
    volatility: float