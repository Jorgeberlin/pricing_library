import numpy as np

from scipy.stats import norm

from hesperides.contracts.european_option import EuropeanOption
from hesperides.contracts.asian_option import AsianOption
from hesperides.market.curves import FlatDiscountCurve

class AnalyticalEngine:

    def price(self, contract, model):

        if isinstance(contract, EuropeanOption):

            S = model.spot
            K = contract.strike
            T = contract.maturity
            sigma = model.volatility
            r = model.risk_free_curve.rate

            df = model.risk_free_curve.df(T)

            d1 = (np.log(S / K)+ (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            if contract.is_call:

                return (S * norm.cdf(d1)- K * df * norm.cdf(d2))

            return (K * df * norm.cdf(-d2)- S * norm.cdf(-d1))
        
        if isinstance(contract, AsianOption):
            pass
        raise TypeError("Unsupported contract type")                 # Meter aquí los siguientes tipos de contrato y modelos, o meterlo en un switch-case o algo así.