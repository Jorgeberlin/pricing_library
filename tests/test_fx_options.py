import pytest
import hesperides.api as hapi

def test_fx_option_call():
    price = hapi.get_price_fx_option(
        St=1.2,
        K=1.2,
        T=1.0,
        r_d=0.05,
        r_f=0.02,
        sigma=0.15,
        call=True,
    )

    assert price == pytest.approx(0.088042475149656, rel=1e-12)


def test_fx_equals_dividend():
    fx = hapi.get_price_fx_option(
        St=1.2,
        K=1.2,
        T=1,
        r_d=0.05,
        r_f=0.02,
        sigma=0.15,
        call=True,
    )

    dividend = hapi.get_price_bs_european_dividend(
        St=1.2,
        K=1.2,
        T=1,
        r=0.05,
        q=0.02,
        sigma=0.15,
        call=True,
    )

    assert fx == pytest.approx(dividend)