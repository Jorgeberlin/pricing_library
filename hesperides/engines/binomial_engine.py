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

        discount = curve.get_discount_factor(dt)

        p = (np.exp(rate * dt) - down) / (up - down)

        j = np.arange(maturity + 1)

        ST = spot * (up ** j) * (down ** (maturity - j))

        if is_call:
            values = np.maximum(ST - strike, 0.0)
        else:
            values = np.maximum(strike - ST, 0.0)

        for _ in range(maturity):

            values = discount * (
                p * values[1:] +
                (1 - p) * values[:-1]
            )

        return float(values[0])