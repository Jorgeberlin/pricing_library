import pytest

import hesperides.api as hapi


def test_bs_european_call():

    price = hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
    )

    assert price == pytest.approx(10.4506, rel=1e-4)

def test_bs_european_put():

    price = hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=False,
    )
    assert price == pytest.approx(5.5735, rel=1e-4)
