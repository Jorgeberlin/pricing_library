from hesperides.contracts.european_option import EuropeanOption
from hesperides.market.curves import FlatDiscountCurve
from hesperides.models.black_scholes_model import BlackScholesModel
from hesperides.greeks.analytical_greek_engine import AnalyticalGreekEngine

contract = EuropeanOption(
    maturity=1.0,
    strike=100,
    is_call=True
)

curve = FlatDiscountCurve(rate=0.05)

model = BlackScholesModel(
    spot=100,
    volatility=0.2,
    risk_free_curve=curve
)

engine = AnalyticalGreekEngine()

print(engine.greek(contract, model, "delta"))
print(engine.greek(contract, model, "gamma"))
print(engine.greek(contract, model, "vega"))
print(engine.greek(contract, model, "rho"))