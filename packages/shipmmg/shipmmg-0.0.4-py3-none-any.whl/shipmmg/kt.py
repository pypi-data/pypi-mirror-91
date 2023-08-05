#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dataclasses
from typing import List
from scipy.misc import derivative
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp


@dataclasses.dataclass
class KTParams:
    """Dataclass for setting KT parameters of KT simulation.

    Attributes:
        K (float): One of parameters in KT model. [1/s]
        T (float): One of parameters in KT model. [s]
    """

    K: float
    T: float


def simulate_kt(
    kt_params: KTParams,
    time_list: List[float],
    delta_list: List[float],
    r0: float = 0.0,
    method: str = "RK45",
    t_eval=None,
    events=None,
    vectorized=False,
    **options
):
    """KT simulation
    KT simulation by following equation of motion.

    :math:`T dr =  -r + K \\delta`

    Args:
        kt_params (KTParams):
            KT parameters.
        time_list (list[float]):
            time list of simulation.
        delta_list (list[float]):
            rudder angle list of simulation.
        r0 (float, optional):
            rate of turn [rad/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        method (str, optional):
            Integration method to use in
            `scipy.integrate.solve_ivp()
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>`_:

                "RK45" (default):
                    Explicit Runge-Kutta method of order 5(4).
                    The error is controlled assuming accuracy of the fourth-order method,
                    but steps are taken using the fifth-order accurate formula (local extrapolation is done).
                    A quartic interpolation polynomial is used for the dense output.
                    Can be applied in the complex domain.
                "RK23":
                    Explicit Runge-Kutta method of order 3(2).
                    The error is controlled assuming accuracy of the second-order method,
                    but steps are taken using the third-order accurate formula (local extrapolation is done).
                    A cubic Hermite polynomial is used for the dense output.
                    Can be applied in the complex domain.
                "DOP853":
                    Explicit Runge-Kutta method of order 8.
                    Python implementation of the “DOP853” algorithm originally written in Fortran.
                    A 7-th order interpolation polynomial accurate to 7-th order is used for the dense output.
                    Can be applied in the complex domain.
                "Radau":
                    Implicit Runge-Kutta method of the Radau IIA family of order 5.
                    The error is controlled with a third-order accurate embedded formula.
                    A cubic polynomial which satisfies the collocation conditions is used for the dense output.
                "BDF":
                    Implicit multi-step variable-order (1 to 5) method
                    based on a backward differentiation formula for the derivative approximation.
                    A quasi-constant step scheme is used and accuracy is enhanced using the NDF modification.
                    Can be applied in the complex domain.
                "LSODA":
                    Adams/BDF method with automatic stiffness detection and switching.
                    This is a wrapper of the Fortran solver from ODEPACK.

        t_eval (array_like or None, optional):
            Times at which to store the computed solution, must be sorted and lie within t_span.
            If None (default), use points selected by the solver.
        events (callable, or list of callables, optional):
            Events to track. If None (default), no events will be tracked.
            Each event occurs at the zeros of a continuous function of time and state.
            Each function must have the signature event(t, y) and return a float.
            The solver will find an accurate value of t at which event(t, y(t)) = 0 using a root-finding algorithm.
            By default, all zeros will be found. The solver looks for a sign change over each step,
            so if multiple zero crossings occur within one step, events may be missed.
            Additionally each event function might have the following attributes:
                terminal (bool, optional):
                    Whether to terminate integration if this event occurs. Implicitly False if not assigned.
                direction (float, optional):
                    Direction of a zero crossing.
                    If direction is positive, event will only trigger when going from negative to positive,
                    and vice versa if direction is negative.
                    If 0, then either direction will trigger event. Implicitly 0 if not assigned.
            You can assign attributes like `event.terminal = True` to any function in Python.
        vectorized (bool, optional):
            Whether `fun` is implemented in a vectorized fashion. Default is False.
        options:
            Options passed to a chosen solver.
            All options available for already implemented solvers are listed in
            `scipy.integrate.solve_ivp()
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>`_:

    Returns:
        Bunch object with the following fields defined:
            t (ndarray, shape (`n_points`,)):
                Time points.
            y (ndarray, shape (`n_points`,)):
                Values of the solution at t.
            sol (OdeSolution):
                Found solution as OdeSolution instance from KT simulation.
            t_events (list of ndarray or None):
                Contains for each event type a list of arrays at which an event of that type event was detected.
                None if events was None.
            y_events (list of ndarray or None):
                For each value of t_events, the corresponding value of the solution.
                None if events was None.
            nfev (int):
                Number of evaluations of the right-hand side.
            njev (int):
                Number of evaluations of the jacobian.
            nlu (int):
                Number of LU decomposition.
            status (int):
                Reason for algorithm termination:
                    - -1: Integration step failed.
                    - 0: The solver successfully reached the end of `tspan`.
                    - 1: A termination event occurred.
            message (string):
                Human-readable description of the termination reason.
            success (bool):
                True if the solver reached the interval end or a termination event occurred (`status >= 0`).

    Examples:
        >>> kt_params = KTParams(K=0.15, T=60.0)
        >>> duration = 300
        >>> num_of_sampling = 3000
        >>> time_list = np.linspace(0.00, duration, num_of_sampling)
        >>> delta_list = 35 * np.pi / 180 * np.sin(3.0 * np.pi / Ts * time_list)
        >>> r0 = 0.0
        >>> sol = simulate_kt(kt_params, time_list, delta_list, r0)
        >>> result = sol.sol(time_list)
    """
    return simulate(
        K=kt_params.K,
        T=kt_params.T,
        time_list=time_list,
        delta_list=delta_list,
        r0=r0,
        method=method,
        t_eval=t_eval,
        events=events,
        vectorized=vectorized,
        **options
    )


def simulate(
    K: float,
    T: float,
    time_list: List[float],
    delta_list: List[float],
    r0: float = 0.0,
    method: str = "RK45",
    t_eval=None,
    events=None,
    vectorized=False,
    **options
):
    """KT simulation
    KT simulation by following equation of motion.

    :math:`T dr =  -r + K \\delta`

    Args:
        K (float):
            parameter K of KT model.
        T (float):
            parameter T of KT model.
        time_list (list[float]):
            time list of simulation.
        delta_list (list[float]):
            rudder angle list of simulation.
        r0 (float, optional):
            rate of turn [rad/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        method (str, optional):
            Integration method to use in
            `scipy.integrate.solve_ivp()
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>`_:

                "RK45" (default):
                    Explicit Runge-Kutta method of order 5(4).
                    The error is controlled assuming accuracy of the fourth-order method,
                    but steps are taken using the fifth-order accurate formula (local extrapolation is done).
                    A quartic interpolation polynomial is used for the dense output.
                    Can be applied in the complex domain.
                "RK23":
                    Explicit Runge-Kutta method of order 3(2).
                    The error is controlled assuming accuracy of the second-order method,
                    but steps are taken using the third-order accurate formula (local extrapolation is done).
                    A cubic Hermite polynomial is used for the dense output.
                    Can be applied in the complex domain.
                "DOP853":
                    Explicit Runge-Kutta method of order 8.
                    Python implementation of the “DOP853” algorithm originally written in Fortran.
                    A 7-th order interpolation polynomial accurate to 7-th order is used for the dense output.
                    Can be applied in the complex domain.
                "Radau":
                    Implicit Runge-Kutta method of the Radau IIA family of order 5.
                    The error is controlled with a third-order accurate embedded formula.
                    A cubic polynomial which satisfies the collocation conditions is used for the dense output.
                "BDF":
                    Implicit multi-step variable-order (1 to 5) method
                    based on a backward differentiation formula for the derivative approximation.
                    A quasi-constant step scheme is used and accuracy is enhanced using the NDF modification.
                    Can be applied in the complex domain.
                "LSODA":
                    Adams/BDF method with automatic stiffness detection and switching.
                    This is a wrapper of the Fortran solver from ODEPACK.

        t_eval (array_like or None, optional):
            Times at which to store the computed solution, must be sorted and lie within t_span.
            If None (default), use points selected by the solver.
        events (callable, or list of callables, optional):
            Events to track. If None (default), no events will be tracked.
            Each event occurs at the zeros of a continuous function of time and state.
            Each function must have the signature event(t, y) and return a float.
            The solver will find an accurate value of t at which event(t, y(t)) = 0 using a root-finding algorithm.
            By default, all zeros will be found. The solver looks for a sign change over each step,
            so if multiple zero crossings occur within one step, events may be missed.
            Additionally each event function might have the following attributes:
                terminal (bool, optional):
                    Whether to terminate integration if this event occurs. Implicitly False if not assigned.
                direction (float, optional):
                    Direction of a zero crossing.
                    If direction is positive, event will only trigger when going from negative to positive,
                    and vice versa if direction is negative.
                    If 0, then either direction will trigger event. Implicitly 0 if not assigned.
            You can assign attributes like `event.terminal = True` to any function in Python.
        vectorized (bool, optional):
            Whether `fun` is implemented in a vectorized fashion. Default is False.
        options:
            Options passed to a chosen solver.
            All options available for already implemented solvers are listed in
            `scipy.integrate.solve_ivp()
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>`_:

    Returns:
        Bunch object with the following fields defined:
            t (ndarray, shape (`n_points`,)):
                Time points.
            y (ndarray, shape (`n_points`,)):
                Values of the solution at t.
            sol (OdeSolution):
                Found solution as OdeSolution instance from KT simulation.
            t_events (list of ndarray or None):
                Contains for each event type a list of arrays at which an event of that type event was detected.
                None if events was None.
            y_events (list of ndarray or None):
                For each value of t_events, the corresponding value of the solution.
                None if events was None.
            nfev (int):
                Number of evaluations of the right-hand side.
            njev (int):
                Number of evaluations of the jacobian.
            nlu (int):
                Number of LU decomposition.
            status (int):
                Reason for algorithm termination:
                    - -1: Integration step failed.
                    - 0: The solver successfully reached the end of `tspan`.
                    - 1: A termination event occurred.
            message (string):
                Human-readable description of the termination reason.
            success (bool):
                True if the solver reached the interval end or a termination event occurred (`status >= 0`).


    Examples:
        >>> K = 0.15
        >>> T = 60.0
        >>> duration = 300
        >>> num_of_sampling = 3000
        >>> time_list = np.linspace(0.00, duration, num_of_sampling)
        >>> delta_list = 35 * np.pi / 180 * np.sin(3.0 * np.pi / Ts * time_list)
        >>> r0 = 0.0
        >>> sol = simulate_kt(K, T, time_list, delta_list, r0)
        >>> result = sol.sol(time_list)
    """
    spl_delta = interp1d(time_list, delta_list, "cubic", fill_value="extrapolate")

    def kt_eom_solve_ivp(t, X, K, T):
        r, delta = X
        d_r = 1.0 / T * (-r + K * delta)
        d_delta = derivative(spl_delta, t)
        return [d_r, d_delta]

    sol = solve_ivp(
        kt_eom_solve_ivp,
        [time_list[0], time_list[-1]],
        [r0, delta_list[0]],
        args=(K, T),
        dense_output=True,
    )
    return sol
