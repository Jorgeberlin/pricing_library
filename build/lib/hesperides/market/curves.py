import numpy as np


class FlatDiscountCurve:
    """
    Flat discount curve with constant risk-free rate.
    """

    def __init__(self, rate: float):
        if rate < 0:
            raise ValueError("Invalid interest rate!!")
        self.rate = rate

    def get_discount_factor(self, t: int) -> float:

        return float(np.exp(-self.rate * t))