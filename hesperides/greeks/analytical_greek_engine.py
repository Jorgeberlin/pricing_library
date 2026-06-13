import numpy as np
from scipy.stats import norm


class AnalyticalGreekEngine:

    def greek(self, contract, model, greek: str) -> float:

        if greek not in {"delta", "gamma", "vega", "rho"}:
            raise ValueError(
                "greek must be one of: delta, gamma, vega, rho"
            )

        S = model.spot
        K = contract.strike
        T = contract.maturity
        sigma = model.volatility
        r = model.risk_free_curve.rate

        d1 = (
            np.log(S / K)
            + (r + 0.5 * sigma**2) * T
        ) / (sigma * np.sqrt(T))

        d2 = d1 - sigma * np.sqrt(T)

        if greek == "delta":

            if contract.is_call:
                return norm.cdf(d1)

            return norm.cdf(d1) - 1.0

        if greek == "gamma":

            return (
                norm.pdf(d1)
                / (S * sigma * np.sqrt(T))
            )

        if greek == "vega":

            return (
                S
                * norm.pdf(d1)
                * np.sqrt(T)
            )

        if greek == "rho":

            df = model.risk_free_curve.df(T)

            if contract.is_call:
                return K * T * df * norm.cdf(d2)

            return -K * T * df * norm.cdf(-d2)