import numpy as np
import pytest
import hesperides.api as hapi

#####################
### AQUÍ METO TODOS LOS CALL-PUT PARITY TESTS QUE SE ME OCURRAN
#####################

def test_dividend_put_call_parity():
    St = 100
    K = 95
    T = 1.5
    r = 0.04
    q = 0.02
    sigma = 0.25

    call = hapi.get_price_bs_european_dividend(
        St=St,
        K=K,
        T=T,
        r=r,
        sigma=sigma,
        call=True,
        q=q,
    )

    put = hapi.get_price_bs_european_dividend(
        St=St,
        K=K,
        T=T,
        r=r,
        sigma=sigma,
        call=False,
        q=q,
    )

    assert call - put == pytest.approx(St * np.exp(-q * T) - K * np.exp(-r * T))