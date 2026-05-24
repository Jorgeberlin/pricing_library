import pytest

import hesperides.api as hapi


def test_mc_european_call():

    price = hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
        engine="mc",
        n_paths=100000,
        seed=1
    )

    assert price == pytest.approx(10.4506, rel= 0.01)

def test_mc_european_put():

    price = hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=False,
        engine="mc",
        n_paths=100000,
        seed=1
    )
    assert price == pytest.approx(5.5735, rel=0.01)