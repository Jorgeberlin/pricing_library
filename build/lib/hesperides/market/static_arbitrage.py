import numpy as np


def vertical_spreads(surface, strikes):
    dC = surface[:-1] - surface[1:]
    dK = np.diff(strikes)[:, None]
    return dC / dK


def calendar_spreads(surface):
    return surface[:, 1:] - surface[:, :-1]


def butterfly_spreads(surface, strikes):

    K_im1 = strikes[:-2]
    K_i = strikes[1:-1]
    K_ip1 = strikes[2:]

    denom = (K_ip1 - K_i)[:, None]

    w_mid = (K_ip1 - K_im1)[:, None] / denom
    w_high = (K_i - K_im1)[:, None] / denom

    return (
        surface[:-2]
        - w_mid * surface[1:-1]
        + w_high * surface[2:]
    )