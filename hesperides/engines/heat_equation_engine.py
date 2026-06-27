import numpy as np
from scipy.linalg import solve_banded


# Función "general" para resolver la ecuación del calor con condiciones de contorno de Dirichlet
# Esta es la base que se usa para resolver funciones ulteriores
def solve_heat_equation(
    initial_condition,
    kappa,
    M,
    T,
    n_x,
    n_t,
    scheme="explicit",
    left_boundary=0.0,
    right_boundary=0.0,
    boundary_type="dirichlet",
):

    # validaciones de los datos para que sean correctos
    if kappa <= 0:
        raise ValueError("kappa must be positive.")

    if M <= 0:
        raise ValueError("M must be positive.")

    if T <= 0:
        raise ValueError("T must be positive.")

    if n_x < 1 or n_t < 1:
        raise ValueError("n_x and n_t must be at least 1.")

    if scheme not in ("explicit", "implicit"):
        raise ValueError("scheme must be 'explicit' or 'implicit'.")

    if boundary_type != "dirichlet":
        raise NotImplementedError(
            "Only Dirichlet boundary conditions are implemented."
        )

    # ======================================================================================================
    # Malla
    dx = M / n_x
    dt = T / n_t

    x = np.linspace(0.0, M, n_x + 1)

    r = kappa * dt / dx**2

    # Solución
    u = np.zeros((n_t + 1, n_x + 1))

    # Condición inicial
    u[0, :] = initial_condition(x)


    # FTCS (explícito)
    if scheme == "explicit":

        for n in range(n_t):

            # Condiciones de contorno (la parte de los nodos exteriores)
            u[n + 1, 0] = left_boundary
            u[n + 1, -1] = right_boundary

            # Nodos interiores
            for j in range(1, n_x):

                u[n + 1, j] = ((1 - 2 * r) * u[n, j] + r * u[n, j - 1]+ r * u[n, j + 1])

    # BTCS (esquema implícito)

    elif scheme == "implicit":

        N = n_x - 1


        ab = np.zeros((3, N))
        ab[0, 1:] = -r
        ab[1, :] = 1 + 2 * r
        ab[2, :-1] = -r

        for n in range(n_t):

            b = u[n, 1:-1].copy()

            b[0] += r * left_boundary
            b[-1] += r * right_boundary

            u[n + 1, 1:-1] = solve_banded((1, 1), ab, b)

            u[n + 1, 0] = left_boundary
            u[n + 1, -1] = right_boundary



    return x, u[-1]


#### AQUÍ METER LAS FUNCIONES QUE TIRAN DEL SOLVER DEL CALOR

def get_price_bs_european_heat(
    St,
    K,
    T,
    r,
    sigma,
    call,
    n_x=400,
    n_t=400,
    scheme="implicit",
):

    # validaciones de los datos
    if St <= 0:
        raise ValueError("St must be positive.")

    if K <= 0:
        raise ValueError("K must be positive.")

    if T <= 0:
        raise ValueError("T must be positive.")

    if sigma <= 0:
        raise ValueError("sigma must be positive.")



    # Dominio del solver del calor
    y_center = (np.log(St) - (sigma**2 / 2 - r) * T) / sigma
    L = 6 * np.sqrt(T)

    y_min = y_center - L
    M = 2 * L

    def initial_condition(x):

        # Trasnformación de la coordenada del solver al dominio y
        y = y_min + x
        S = np.exp(sigma * y)

        if call:
            return np.maximum(S - K, 0.0)
        return np.maximum(K - S, 0.0)
    

    y_grid, G = solve_heat_equation(
        initial_condition=initial_condition,
        kappa=0.5,
        M=M,
        T=T,
        n_x=n_x,
        n_t=n_t,
        scheme=scheme,
        left_boundary=0.0 if call else K,
        right_boundary=max(np.exp(sigma * (y_min + M)) - K, 0.0) if call else 0.0,
    )
    
    # Punto correspondiente al spot actual en la variable transformada
    y0 = (np.log(St) - (sigma**2 / 2 - r) * T) / sigma
    x0 = y0 - y_min

    # Interpolamos la solución numérica sobre ese punto
    G0 = np.interp(x0, y_grid, G)

    # Deshacemos la transformación para obtener el precio
    price = np.exp(-r * T) * G0

    return price




