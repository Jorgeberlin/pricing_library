import pytest

import hesperides.api as hapi

#TODO: Meter un diccionario de precios y testear con eso.

def test_mc_geometric_asian_call():
    price = hapi.get_price_bs_geometric_asian(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
        engine="mc",
        n_paths=500000,
        n_steps=100,
        seed=1
    )

    assert price == pytest.approx(5.5468, rel=0.01)
    assert price < hapi.get_price_bs_european(           # Mismo test que para el analítico, solo que ahora revisando para Monte Carlo (y con tolerancia un poquito más alta).
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
        engine="mc",
        n_paths=500000,
        seed=1
    )

def test_mc_geometric_asian_put():

    price = hapi.get_price_bs_geometric_asian(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=False,
        engine="mc",
        n_paths=500000,
        n_steps=100,
        seed=1
    )

    assert price == pytest.approx(3.47, rel=1e-2)