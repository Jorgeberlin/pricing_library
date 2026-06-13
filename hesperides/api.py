# Módulos necesarios para el cálculo de cantidades de arbitraje estático
from __future__ import annotations

# Módulos necesarios para el pricing
from hesperides.contracts.asian_option import AsianOption
from hesperides.contracts.european_option import EuropeanOption
from hesperides.engines.monte_carlo_engine import MonteCarloEngine
from hesperides.models.binomial_model import BinomialModel
from hesperides.models.black_scholes_model import BlackScholesModel
from hesperides.pricers.binomial_pricer import BinomialPricer
from hesperides.engines.analytical_engine import AnalyticalEngine
from hesperides.market.curves import FlatDiscountCurve

# Los imports para las griegas
from hesperides.greeks.analytical_greek_engine import AnalyticalGreekEngine
from hesperides.greeks.fd_greek_engine import FiniteDifferenceGreekEngine

"""
Public API for the pricing library.
"""

# BINOMIAL FACHADA DE API
def get_price_binomial_european(
    St: float,
    K: float,
    T: int,
    R: float,
    u: float,
    d: float,
    call: bool,
) -> float:

    contract = EuropeanOption(
        strike=K,
        maturity=T,
        is_call=call,
    )

    model = BinomialModel(
        spot=St,
        rate=R,
        up=u,
        down=d,
    )

    return BinomialPricer.price(
        contract=contract,
        model=model,
    )



"""
Public API for the static arbitrage quantities on call surfaces.
"""

# FACHADA DE API PARA CANTIDADES DE ARBITRAJE ESTÁTICO EN SUPERFICIES DE CALLS

from hesperides.market.static_arbitrage import (
    vertical_spreads,
    butterfly_spreads,
    calendar_spreads,
)


def compute_static_arbitrage_quantity(
    surface,
    strikes=None,
    quantity="vertical",
):

    if quantity == "vertical":
        return vertical_spreads(surface, strikes)

    if quantity == "butterfly":
        return butterfly_spreads(surface, strikes)

    if quantity == "calendar":
        return calendar_spreads(surface)

    raise ValueError("Invalid quantity")

#  FACHADA PARA BLACK-SCHOLES:

def get_price_bs_european(
    St: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    call: bool,
    engine: str = "analytical",
    n_paths: int | None = None,
    seed: int | None = None,
) -> float:
    """
    Price a European option (call or put) under Black–Scholes.

    Parameters
    ----------
    St : float
        Spot price of the underlying at valuation date.
    K : float
        Strike.
    T : float
        Time to maturity in years.
    r : float
        Continuously compounded risk-free rate.
    sigma : float
        Black–Scholes volatility (annualized).
    call : bool
        True for call, False for put.
    engine : {"analytical", "mc"}, optional
        Pricing engine. Default "analytical".
    n_paths : int or None, optional
        Number of Monte Carlo paths. Required if engine="mc";
        ignored if engine="analytical".
    seed : int or None, optional
        Seed for reproducible Monte Carlo.

    Returns
    -------
    float
        Option price at valuation date.
    """

    curve = FlatDiscountCurve(r)
    model = BlackScholesModel(spot=St, volatility=sigma, risk_free_curve=curve)
    contract = EuropeanOption(maturity=T, strike=K, is_call=call)

    if engine == "analytical":
        pricing_engine = AnalyticalEngine()
        return pricing_engine.price(contract, model)
    
    elif engine == "mc":
        if n_paths is None:
            raise ValueError("n_paths is required for Monte Carlo")
        pricing_engine = MonteCarloEngine()
        return pricing_engine.price(contract, model, n_paths = n_paths, seed=seed)
    
    else:
        raise ValueError("Invalid engine")


#Fachada para la asiática geométrica:

def get_price_bs_geometric_asian(
    St: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    call: bool,
    engine: str = "analytical",
    n_paths: int | None = None,
    n_steps: int | None = None,
    seed: int | None = None,
) -> float:
    curve = FlatDiscountCurve(r)
    model = BlackScholesModel(spot=St, volatility=sigma, risk_free_curve=curve)
    contract = AsianOption(maturity=T, strike=K, is_call=call, is_geom=True)
    if engine == "analytical":
        pricing_engine = AnalyticalEngine()
        return pricing_engine.price(contract, model)

    elif engine == "mc":
        if n_paths is None:
            raise ValueError("n_paths is required for Monte Carlo")
        if n_steps is None:
            raise ValueError("n_steps is required for Monte Carlo Asian")
        pricing_engine = MonteCarloEngine()
        return pricing_engine.price(contract, model, n_paths=n_paths, n_steps=n_steps, seed=seed)
    
# API fachada para las griegas:
def get_greek_bs_european(
    St: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    call: bool,
    greek: str,
    engine: str = "analytical",
    greek_engine: str = "analytical",
    fd_scheme: str = "central",
    h: float | None = None,
    n_paths: int | None = None,
    seed: int | None = None,
) -> float:

    # Validaciones para los datos

    if greek not in {"delta", "gamma", "vega", "rho"}:
        raise ValueError("Invalid greek")

    if engine not in {"analytical", "mc"}:
        raise ValueError("Invalid engine")

    if greek_engine not in {"analytical", "fd"}:
        raise ValueError("Invalid greek_engine")

    # Market/model validaciones

    if St <= 0:
        raise ValueError("St must be positive")

    if K <= 0:
        raise ValueError("K must be positive")

    if T <= 0:
        raise ValueError("T must be positive")

    if sigma <= 0:
        raise ValueError("sigma must be positive")

    # FD-specific validation

    if greek_engine == "fd":

        if fd_scheme not in {"forward", "central"}:
            raise ValueError("Invalid fd_scheme")

        if h is not None and h <= 0:
            raise ValueError("h must be positive")

        if engine == "mc":

            if n_paths is None or n_paths <= 0:
                raise ValueError("n_paths must be positive")

            if seed is None:
                raise ValueError("seed is required for FD Monte Carlo Greeks")

    # Los objetos los pongo aquí

    curve = FlatDiscountCurve(r)
    model = BlackScholesModel(spot=St,volatility=sigma,risk_free_curve=curve)
    contract = EuropeanOption(maturity=T,strike=K,is_call=call)

    # Analytical Greeks

    if greek_engine == "analytical":

        greek_calc = AnalyticalGreekEngine()
        return greek_calc.greek(contract=contract,model=model,greek=greek)

    # FD Greeks

    if engine == "analytical":

        greek_calc = FiniteDifferenceGreekEngine(AnalyticalEngine())

    else:

        greek_calc = FiniteDifferenceGreekEngine(MonteCarloEngine())

    return greek_calc.greek(
        contract=contract,
        model=model,
        greek=greek,
        scheme=fd_scheme,
        h=h,
        n_paths=n_paths,
        seed=seed
    )