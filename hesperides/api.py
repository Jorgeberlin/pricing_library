from hesperides.contracts.european_option import EuropeanOption
from hesperides.models.binomial_model import BinomialModel
from hesperides.pricers.binomial_pricer import BinomialPricer

"""
Public API for the pricing library.
"""
# Este lo dejo aquí para tener como base (por si necesito pasar 1 dummy test al menos)
def health_check() -> str:
    return "ok"

#Este es el test de Romaniega, está en el github de la entrega
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