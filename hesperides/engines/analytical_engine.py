import numpy as np
from scipy.stats import norm

from hesperides.contracts.european_option import EuropeanOption
from hesperides.contracts.asian_option import AsianOption
from hesperides.market.curves import FlatDiscountCurve



class AnalyticalEngine:

    def price(self, contract, model):

        # Aquí me pongo los paramétros que son comunes y solo cambio los parámetros específicos.
        S = model.spot
        K = contract.strike
        T = contract.maturity
        sigma = model.volatility
        r = model.risk_free_curve.rate
        df = model.risk_free_curve.df(T)
        q = model.dividend_yield

        if isinstance(contract, EuropeanOption):

            d1 = (np.log(S/K)+ (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            if contract.is_call:
                return S * np.exp(-q * T) * norm.cdf(d1) - K * df * norm.cdf(d2)
            return K * df * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)

        elif isinstance(contract, AsianOption):

            if contract.is_geom:

                sigma_g = sigma / np.sqrt(3)
                mu_g = 0.5 * (r - q - sigma**2 / 6)

                d1 = (np.log(S / K) + (mu_g + 0.5 * sigma_g**2) * T) / (sigma_g * np.sqrt(T))
                d2 = d1 - sigma_g * np.sqrt(T)

                if contract.is_call:
                    return df * (S * np.exp(mu_g * T) * norm.cdf(d1) - K * norm.cdf(d2))
                return df * (K * norm.cdf(-d2) - S * np.exp(mu_g * T) * norm.cdf(-d1))

        raise TypeError("Unsupported contract type")                 # Ir metiendo aquí los siguientes tipos de contrato y modelos.