from random import seed

from hesperides.models.black_scholes_model import BlackScholesModel
from hesperides.engines.monte_carlo_engine import MonteCarloEngine
from hesperides.market.curves import FlatDiscountCurve


class FiniteDifferenceGreekEngine:

    def __init__(self, pricing_engine):
        self.pricing_engine = pricing_engine

    def _price(self, contract, model, n_paths=None, seed=None) -> float:

        if isinstance(self.pricing_engine, MonteCarloEngine):            # Aquí meter elif si la cosa se empieza a complicar en el futuro.
            return self.pricing_engine.price(contract, model, n_paths=n_paths, seed=seed)

        return self.pricing_engine.price(contract, model)

    def greek(self, contract, model, greek: str, scheme: str = "central", h: float | None = None, n_paths: int | None = None, seed: int | None = None):

        if greek not in {"delta", "gamma", "vega", "rho"}:
            raise ValueError("Solo se han implementado delta, gamma, vega y rho.")

        if scheme not in {"central", "forward"}:
            raise ValueError("Solo hay esquemas forward y central implementados.")

        if greek in {"delta", "gamma"}:

            if h is not None and h <= 0:
                raise ValueError("h tiene que ser positivo")
            if h is None:
                h = 0.01 * model.spot

            model_up = BlackScholesModel(
                spot=model.spot + h,
                volatility=model.volatility,
                risk_free_curve=model.risk_free_curve
            )

            model_down = BlackScholesModel(
                spot=model.spot - h,
                volatility=model.volatility,
                risk_free_curve=model.risk_free_curve
            )

            price_up = self._price(contract, model_up, n_paths=n_paths, seed=seed)

            price_down = self._price(contract, model_down, n_paths=n_paths, seed=seed)

        if greek == "delta":                         # Si se van a hacer más esquemas, meterlos en un elif.

            if scheme == "forward":

                price_mid = self._price(contract, model, n_paths=n_paths, seed=seed)

                return (price_up - price_mid) / h

            return (price_up - price_down) / (2 * h)
        
        if greek == "gamma":

            price_mid = self._price(contract, model, n_paths=n_paths, seed=seed)

            return (price_up - 2 * price_mid + price_down) / (h ** 2)
        
        if greek == "vega":

            if h is None:
                h = 0.00001  #Simplemente porque la volatilidad ya está en porcentaje.

            model_up = BlackScholesModel(spot=model.spot, volatility=model.volatility + h, risk_free_curve=model.risk_free_curve)

            model_down = BlackScholesModel(spot=model.spot, volatility=model.volatility - h, risk_free_curve=model.risk_free_curve)

            price_up = self._price(contract, model_up, n_paths=n_paths, seed=seed)

            price_down = self._price(contract, model_down, n_paths=n_paths, seed=seed)

            if scheme == "forward":                                                   # Si se van a hacer más esquemas, meterlos en un elif.

                price_mid = self._price(contract, model, n_paths=n_paths, seed=seed)

                return (price_up - price_mid) / h

            return (price_up - price_down) / (2 * h)
        
        if greek == "rho":                                     # Misma implementación. Simplemente hay que cambiar la curva (curva plana de momento) que se usa por la bumpeada para ser consistentes.

            if h is None:
                h = 0.0001

            curve_up = FlatDiscountCurve(model.risk_free_curve.rate + h)

            curve_down = FlatDiscountCurve(model.risk_free_curve.rate - h)

            model_up = BlackScholesModel(spot=model.spot, volatility=model.volatility, risk_free_curve=curve_up)

            model_down = BlackScholesModel(spot=model.spot, volatility=model.volatility, risk_free_curve=curve_down)

            price_up = self._price(contract, model_up, n_paths=n_paths, seed=seed)

            price_down = self._price(contract, model_down, n_paths=n_paths, seed=seed)

            if scheme == "forward":

                price_mid = self._price(contract, model, n_paths=n_paths, seed=seed)

                return (price_up - price_mid) / h

            return (price_up - price_down) / (2 * h)
