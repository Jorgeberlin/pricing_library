import numpy as np

from hesperides.contracts.european_option import EuropeanOption
from hesperides.contracts.asian_option import AsianOption


class MonteCarloEngine:

    def price(self, contract, model, n_paths, n_steps=None, seed=None) -> float:

        if isinstance(contract, EuropeanOption):

            S = model.spot
            K = contract.strike
            T = contract.maturity
            sigma = model.volatility
            r = model.risk_free_curve.rate
            df = model.risk_free_curve.df(T)

            rng = np.random.default_rng(seed)
            z = rng.standard_normal(n_paths)
            ST = S * np.exp((r - 0.5 * sigma**2) * T+ sigma * np.sqrt(T) * z)

            if contract.is_call:
                payoff = np.maximum(ST - K, 0)

            else:
                payoff = np.maximum(K - ST, 0)

            return df * payoff.mean()

        raise TypeError("Unsupported contract type")