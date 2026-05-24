import pytest

import hesperides.api as hapi


def test_mc_european_call():

    list_n_paths = [100, 1000000]   # Aquí puedes meter los que se quieran, pero dejé 2 porque en realidad este test puede romperse por casualidad. 
    prices = []                     # Para comprobar la convergencia realmente hace falta un análisis estadístico más complejo, pero con esto   
    for path in list_n_paths:       # ya se puede ver que el precio con más paths es más cercano al analítico que el precio con menos paths.
        prices.append(hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        call=True,
        engine="mc",
        n_paths=path,
        seed=1))

    assert abs(prices[0] - 10.4506) > abs(prices[1] - 10.4506)
