import numpy as np

from hesperides.market.curves import FlatDiscountCurve


class BinomialEngine:

    @staticmethod
    def price(
        spot: float,
        strike: float,
        maturity: int,
        rate: float,
        up: float,
        down: float,
        is_call: bool,
    ) -> float:

        curve = FlatDiscountCurve(rate)

        dt = 1.0

        discount = curve.get_simple_discount_factor(dt)

        prob_risk_neutral= (1.0 + rate - down) / (up - down)

        t = np.arange(maturity + 1)

        st = spot * (up ** t) * (down ** (maturity - t))

        if is_call == True:
            values = np.maximum(st - strike, 0.0)
        else:
            values = np.maximum(strike - st, 0.0)

        for _ in range(maturity):

            values = discount * (
                prob_risk_neutral * values[1:] +
                (1 - prob_risk_neutral) * values[:-1]
            )

        return float(values[0])