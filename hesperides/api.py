# Módulos necesarios para el cálculo de cantidades de arbitraje estático
from __future__ import annotations

# Módulos necesarios para el pricing
from hesperides.contracts.european_option import EuropeanOption
from hesperides.models.binomial_model import BinomialModel
from hesperides.models.black_scholes_model import BlackScholesModel
from hesperides.pricers.binomial_pricer import BinomialPricer
from hesperides.engines.analytical_engine import AnalyticalEngine
from hesperides.market.curves import FlatDiscountCurve

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

    model = BlackScholesModel(
    spot=St,
    volatility=sigma,
    risk_free_curve=curve)

    contract = EuropeanOption(
    maturity=T,
    strike=K,
    is_call=call)

    pricing_engine = AnalyticalEngine()

    return pricing_engine.price(contract, model)
