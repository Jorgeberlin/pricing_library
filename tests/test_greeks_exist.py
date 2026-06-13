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




from hesperides.contracts.european_option import EuropeanOption
from hesperides.market.curves import FlatDiscountCurve
from hesperides.models.black_scholes_model import BlackScholesModel

from hesperides.engines.analytical_engine import AnalyticalEngine
from hesperides.greeks.analytical_greek_engine import AnalyticalGreekEngine
from hesperides.greeks.fd_greek_engine import FiniteDifferenceGreekEngine


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

analytical = AnalyticalGreekEngine().greek(
    contract,
    model,
    "delta"
)

fd = FiniteDifferenceGreekEngine(
    AnalyticalEngine()
).greek(
    contract,
    model,
    greek="delta"
)

print(analytical)
print(fd)


#########################################
gamma_analytical = AnalyticalGreekEngine().greek(
    contract,
    model,
    "gamma"
)

gamma_fd = FiniteDifferenceGreekEngine(
    AnalyticalEngine()
).greek(
    contract,
    model,
    "gamma"
)

print(gamma_analytical)
print(gamma_fd)


#######rho
rho_analytical = AnalyticalGreekEngine().greek(contract, model, "rho")

rho_fd = FiniteDifferenceGreekEngine(AnalyticalEngine()).greek(contract, model, "rho")

print(rho_analytical)
print(rho_fd)