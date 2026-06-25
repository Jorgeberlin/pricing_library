import numpy as np

from hesperides.contracts.european_option import EuropeanOption
from hesperides.contracts.asian_option import AsianOption


class MonteCarloEngine:

    def price(self, contract, model, n_paths, n_steps=None, seed=None) -> float:
        # Aquí meto los atributos comunes (para no andar repitiendo código)
        S = model.spot
        K = contract.strike
        T = contract.maturity 
        sigma = model.volatility
        r = model.risk_free_curve.rate
        df = model.risk_free_curve.df(T)
        q = model.dividend_yield

        if isinstance(contract, EuropeanOption):

            rng = np.random.default_rng(seed)
            z = rng.standard_normal(n_paths)
            ST = S * np.exp((r - q - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)

            if contract.is_call:
                payoff = np.maximum(ST - K, 0)

            else:
                payoff = np.maximum(K - ST, 0)

            return df * payoff.mean()

        elif isinstance(contract, AsianOption):

            if n_steps is None:
                raise ValueError("n_steps is required for Asian Monte Carlo")

            dt = T / n_steps

            rng = np.random.default_rng(seed)
            z = rng.standard_normal((n_paths, n_steps))
            log_returns = (r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
            log_paths = np.cumsum(log_returns, axis=1)                        # Sumamos los log_returns
            paths = S * np.exp(log_paths)                                     # Obtenemos los paths a partir de los log_paths (convierto a precios a partir de la trayectoria)
            geo_mean = np.exp(np.mean(np.log(paths), axis=1))

            if contract.is_call:
                payoff = np.maximum(geo_mean - K, 0)

            else:
                payoff = np.maximum(K - geo_mean, 0)

            return df * payoff.mean()
        
        raise TypeError("Unsupported contract type")