# Módulos necesarios para el cálculo de cantidades de arbitraje estático
from __future__ import annotations

# Módulos necesarios para el pricing
from hesperides.contracts.european_option import EuropeanOption
from hesperides.models.binomial_model import BinomialModel
from hesperides.pricers.binomial_pricer import BinomialPricer

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
