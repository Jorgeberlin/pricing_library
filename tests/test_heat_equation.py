import numpy as np
from numpy.testing import assert_allclose

import hesperides.api as hapi


def test_heat_equation_matches_exact_solution_explicit():

    M = 1.0
    kappa = 0.1
    T = 0.5

    n_x = 200
    n_t = 4000

    def f(x):
        return np.sin(np.pi * x / M)

    x, u = hapi.solve_heat_equation(
        initial_condition=f,
        kappa=kappa,
        M=M,
        T=T,
        n_x=n_x,
        n_t=n_t,
        scheme="explicit",
    )

    exact = (
        np.exp(-kappa * (np.pi / M) ** 2 * T)
        * np.sin(np.pi * x / M)
    )
    max_error = np.max(np.abs(u - exact))
    print(max_error)

    assert_allclose(u, exact, atol=1e-2)



def test_heat_equation_matches_exact_solution_implicit():

    M = 1.0
    kappa = 0.1
    T = 0.5

    n_x = 200
    n_t = 100

    def f(x):
        return np.sin(np.pi * x / M)

    x, u = hapi.solve_heat_equation(
        initial_condition=f,
        kappa=kappa,
        M=M,
        T=T,
        n_x=n_x,
        n_t=n_t,
        scheme="implicit",
    )

    exact = (
        np.exp(-kappa * (np.pi / M) ** 2 * T)
        * np.sin(np.pi * x / M)
    )

    assert_allclose(u, exact, atol=1e-2)



def test_heat_matches_black_scholes_call():

    price_heat = hapi.get_price_bs_european_heat(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.20,
        call=True,
    )

    price_bs = hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.20,
        call=True,
    )

    assert_allclose(price_heat, price_bs, atol=1e-2)


def test_heat_matches_black_scholes_put():

    price_heat = hapi.get_price_bs_european_heat(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.20,
        call=False,
    )

    price_bs = hapi.get_price_bs_european(
        St=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.20,
        call=False,
    )

    assert_allclose(price_heat, price_bs, atol=1e-2)