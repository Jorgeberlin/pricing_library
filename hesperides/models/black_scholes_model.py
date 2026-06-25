from dataclasses import dataclass

from hesperides.market.curves import FlatDiscountCurve


@dataclass(slots=True)
class BlackScholesModel:

    spot: float
    volatility: float
    risk_free_curve: FlatDiscountCurve
    dividend_yield: float = 0.0