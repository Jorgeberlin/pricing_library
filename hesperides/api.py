"""
Public API for the pricing library.
"""

def health_check() -> str:
    return "ok"

def get_price_binomial_european(
    St: float,
    K: float,
    T: int,
    R: float,
    u: float,
    d: float,
    call: bool,
) -> float:
    """
    Price a European call or put option using the binomial model.

    Parameters
    ----------
    St : float
        Spot price of the underlying at time t.
    K : float
        Strike price.
    T : int
        Number of time steps to maturity.
    R : float
        Risk-free rate (per period).
    u : float
        Up factor.
    d : float
        Down factor.
    call : bool
        If True, price a call option; if False, price a put option.

    Returns
    -------
    float
        Option price at time t.
    """
    ...