import numpy as np


class FlatDiscountCurve:

    def __init__(self, rate: float):

        self.rate = rate

    def get_simple_discount_factor(self, t: float) -> float:

        return 1.0 / (1.0 + self.rate) ** t