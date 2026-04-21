# Módulos necesarios para el cálculo de cantidades de arbitraje estático
from __future__ import annotations
import numpy as np

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



def compute_static_arbitrage_quantity(
    surface: np.ndarray,
    strikes: np.ndarray | None = None,
    quantity: str = "vertical",
) -> np.ndarray:

    if quantity not in {"vertical", "butterfly", "calendar"}:
        raise ValueError(
            "quantity must be 'vertical', 'butterfly', or 'calendar'"
        )

    surface = np.asarray(surface, dtype=float)

    if surface.ndim != 2:
        raise ValueError("surface must be 2D")

    nK, nT = surface.shape

    # ---------------------------------
    # CALENDAR
    # ---------------------------------

    if quantity == "calendar":

        if nT < 2:
            raise ValueError("Need at least two maturities")

        return surface[:, 1:] - surface[:, :-1]

    # ---------------------------------
    # STRIKE VALIDATION
    # ---------------------------------

    if strikes is None:
        raise ValueError(
            "strikes required for vertical and butterfly"
        )

    strikes = np.asarray(strikes, dtype=float)

    if strikes.ndim != 1:
        raise ValueError("strikes must be 1D")

    if len(strikes) != nK:
        raise ValueError(
            "strikes length must match surface rows"
        )

    if not np.all(np.diff(strikes) > 0):
        raise ValueError(
            "strikes must be strictly increasing"
        )

    # ---------------------------------
    # VERTICAL
    # ---------------------------------

    if quantity == "vertical":

        dC = surface[:-1, :] - surface[1:, :]
        dK = np.diff(strikes)[:, None]

        return dC / dK

    # ---------------------------------
    # BUTTERFLY
    # ---------------------------------

    if quantity == "butterfly":

        if nK < 3:
            raise ValueError(
                "Need at least three strikes"
            )

        K_im1 = strikes[:-2]
        K_i = strikes[1:-1]
        K_ip1 = strikes[2:]

        denom = (K_ip1 - K_i)[:, None]

        weight_mid = (
            (K_ip1 - K_im1)[:, None] / denom
        )

        weight_high = (
            (K_i - K_im1)[:, None] / denom
        )

        C_im1 = surface[:-2, :]
        C_i = surface[1:-1, :]
        C_ip1 = surface[2:, :]

        BS = (
            C_im1
            - weight_mid * C_i
            + weight_high * C_ip1
        )

        return BS