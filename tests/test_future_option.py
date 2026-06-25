import pytest
import hesperides.api as hapi

def test_future_option_call():
    price = hapi.get_price_future_option(
        F0=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.20,
        call=True,
    )

    assert price == pytest.approx(7.57708214642728)


def test_future_equals_dividend_model():
    future_price = hapi.get_price_future_option(
        F0=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.20,
        call=True,
    )

    dividend_price = hapi.get_price_bs_european_dividend(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.20,
        q=0.05,
        call=True,
    )

    assert future_price == pytest.approx(dividend_price)