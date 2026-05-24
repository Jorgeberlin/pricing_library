import pytest

import hesperides.api as hapi

#TODO: Meter un diccionario de precios y testear con eso.

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

def test_bs_geometric_asian_call():
    price = hapi.get_price_bs_geometric_asian(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
    )

    assert price == pytest.approx(5.5468, rel=1e-4)
    assert price < hapi.get_price_bs_european(           # Este test lo meto porque el precio de la asiática geométrica tiene que ser menor que el de la europea.
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
    )