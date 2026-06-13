import pytest
import hesperides.api as hapi
import numpy as np

@pytest.mark.parametrize(
    "greek, expected",
    [
        ("delta", 0.6368306512),
        ("gamma", 0.0187620173),
        ("vega", 37.52403469),
        ("rho", 53.23248155),
    ],
)
def test_analytical_call_greeks_regression(greek, expected):

    value = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek=greek,
        greek_engine="analytical",
    )

    assert value == pytest.approx(expected, rel=1e-6)


@pytest.mark.parametrize(
    "greek",
    ["delta", "gamma", "vega", "rho"]
)
def test_fd_analytical_matches_closed_form(greek):  #testeo analitico sobre diferencias finitas

    analytical = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek=greek,
        greek_engine="analytical"
    )

    fd = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek=greek,
        greek_engine="fd",
        engine="analytical",
        fd_scheme="central"
    )

    assert fd == pytest.approx(analytical, rel=1e-3)


def test_fd_mc_delta_matches_analytical():         #testeo montecarlo sobre analitico

    analytical_delta = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek="delta",
        greek_engine="analytical"
    )

    fd_mc_delta = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek="delta",
        greek_engine="fd",
        engine="mc",
        n_paths=100_000,
        seed=123
    )

    assert fd_mc_delta == pytest.approx(
        analytical_delta,
        rel=5e-2
    )



def test_greek_call_put_parity(): # para testear las paridades que se dan en las griegas.

    K = 100
    T = 1
    r = 0.05

    delta_call = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=True, greek="delta"
    )

    delta_put = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=False, greek="delta"
    )

    assert delta_call - delta_put == pytest.approx(1.0, rel=1e-6)

    gamma_call = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=True, greek="gamma"
    )

    gamma_put = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=False, greek="gamma"
    )

    assert gamma_call == pytest.approx(gamma_put, rel=1e-6)

    vega_call = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=True, greek="vega"
    )

    vega_put = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=False, greek="vega"
    )

    assert vega_call == pytest.approx(vega_put, rel=1e-6)

    rho_call = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=True, greek="rho"
    )

    rho_put = hapi.get_greek_bs_european(
        St=100, K=K, T=T, r=r, sigma=0.2,
        call=False, greek="rho"
    )

    expected = K * T * np.exp(-r * T)

    assert rho_call - rho_put == pytest.approx(
        expected,
        rel=1e-6
    )


def test_negative_h_raises():

    with pytest.raises(ValueError):

        hapi.get_greek_bs_european(
            St=100,
            K=100,
            T=1,
            r=0.05,
            sigma=0.2,
            call=True,
            greek="delta",
            greek_engine="fd",
            h=-1
        )


def test_rho_consistency():

    analytical_rho = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek="rho",
        greek_engine="analytical"
    )

    fd_rho = hapi.get_greek_bs_european(
        St=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
        call=True,
        greek="rho",
        greek_engine="fd",
        engine="analytical"
    )

    assert fd_rho == pytest.approx(
        analytical_rho,
        rel=1e-3
    )