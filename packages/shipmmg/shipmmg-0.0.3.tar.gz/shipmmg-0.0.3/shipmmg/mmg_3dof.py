#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dataclasses
from typing import List
import numpy as np
from scipy.misc import derivative
from scipy.interpolate import interp1d
from scipy.integrate import odeint


@dataclasses.dataclass
class Mmg3DofBasicParams:
    """Dataclass for setting basic parameters of MMG 3ODF.

    Attributes:
        L_pp (float):
            Ship length between perpendiculars [m]
        B (float):
            Ship breadth [m]
        d (float):
            Ship draft [m]
        nabla (float):
            Displacement volume of ship [m^3]
        x_G (float):
            Longitudinal coordinate of center of gravity of ship [-]
        D_p (float):
            Propeller diameter [m]
        m_ (float):
            Ship mass (non-dimensionalized) [-]
        I_zG (float):
            Moment of inertia of ship around center of gravity [-]
        Λ (float):
            Rudder aspect ratio [-]
        A_R_Ld (float):
            Profile area of movable part of mariner rudder[-]
        η (float):
            Ratio of propeller diameter to rudder span (=D_p/HR)
        m_x_ (float):
            Added masses of x axis direction (non-dimensionalized)
        m_y_ (float):
            Added masses of y axis direction (non-dimensionalized)
        J_z (float):
            Added moment of inertia (non-dimensionalized)
        f_α (float):
            Rudder lift gradient coefficient
        ϵ (float):
            Ratio of wake fraction at propeller and rudder positions
        t_R (float):
            Steering resistance deduction factor
        a_H (float):
            Rudder force increase factor
        x_H (float):
            Longitudinal coordinate of acting point of the additional lateral force component induced by steering
        γ_R (float):
            Flow straightening coefficient
        l_R (float):
            Effective longitudinal coordinate of rudder position in formula of βR
        κ (float):
            An experimental constant for　expressing uR
        t_P (float):
            Thrust deduction factor
        w_P0 (float):
            Wake coefficient at propeller position in straight moving

    Note:
        For more information, please see the following articles.

        - Yasukawa, H., Yoshimura, Y. (2015) Introduction of MMG standard method for ship maneuvering predictions.
          J Mar Sci Technol 20, 37–52 https://doi.org/10.1007/s00773-014-0293-y
    """

    L_pp: float
    B: float
    d: float
    nabla: float
    x_G: float
    D_p: float
    m_: float
    I_zG: float
    Λ: float
    A_R_Ld: float
    η: float
    m_x_: float
    m_y_: float
    J_z: float
    f_α: float
    ϵ: float
    t_R: float
    a_H: float
    x_H: float
    γ_R: float
    l_R: float
    κ: float
    t_P: float
    w_P0: float


@dataclasses.dataclass
class Mmg3DofManeuveringParams:
    """Dataclass for setting maneuvering parameters of MMG 3ODF.

    Attributes:
        C_1 (float): One of manuevering parameters of MMG 3DOF
        C_2 (float): One of manuevering parameters of MMG 3DOF
        C_3 (float): One of manuevering parameters of MMG 3DOF
        X_0 (float): One of manuevering parameters of MMG 3DOF
        X_ββ (float): One of manuevering parameters of MMG 3DOF
        X_βγ (float): One of manuevering parameters of MMG 3DOF
        X_γγ (float): One of manuevering parameters of MMG 3DOF
        X_ββββ (float): One of manuevering parameters of MMG 3DOF
        Y_β (float): One of manuevering parameters of MMG 3DOF
        Y_γ (float): One of manuevering parameters of MMG 3DOF
        Y_βββ (float): One of manuevering parameters of MMG 3DOF
        Y_ββγ (float): One of manuevering parameters of MMG 3DOF
        Y_βγγ (float): One of manuevering parameters of MMG 3DOF
        Y_γγγ (float): One of manuevering parameters of MMG 3DOF
        N_β (float): One of manuevering parameters of MMG 3DOF
        N_γ (float): One of manuevering parameters of MMG 3DOF
        N_βββ (float): One of manuevering parameters of MMG 3DOF
        N_ββγ (float): One of manuevering parameters of MMG 3DOF
        N_βγγ (float): One of manuevering parameters of MMG 3DOF
        N_γγγ (float): One of manuevering parameters of MMG 3DOF

    Note:
        For more information, please see the following articles.

        - Yasukawa, H., Yoshimura, Y. (2015) Introduction of MMG standard method for ship maneuvering predictions.
          J Mar Sci Technol 20, 37–52 https://doi.org/10.1007/s00773-014-0293-y
    """

    C_1: float
    C_2: float
    C_3: float
    X_0: float
    X_ββ: float
    X_βγ: float
    X_γγ: float
    X_ββββ: float
    Y_β: float
    Y_γ: float
    Y_βββ: float
    Y_ββγ: float
    Y_βγγ: float
    Y_γγγ: float
    N_β: float
    N_γ: float
    N_βββ: float
    N_ββγ: float
    N_βγγ: float
    N_γγγ: float


def simulate_mmg_3dof(
    basic_params: Mmg3DofBasicParams,
    maneuvering_params: Mmg3DofManeuveringParams,
    R_0_func: interp1d,
    time_list: List[float],
    delta_list: List[float],
    npm_list: List[float],
    u0: float = 0.0,
    v0: float = 0.0,
    r0: float = 0.0,
    ρ: float = 1.025,
) -> np.ndarray:
    """MMG 3DOF simulation
    MMG 3DOF simulation by follwoing equation of motion.

    .. math::

        m (\dot{u}-vr)&=-m_x\dot{u}+m_yvr+X_H+R_0+X_P+X_R

        m (\dot{v}+ur)&=-m_y\dot{v}+m_xur+Y_H+Y_R

        I_{zG}\dot{r}&=-J_Z\dot{r}+N_H+N_R

    Args:
        basic_params (Mmg3DofBasicParams):
            Basic paramters for MMG 3DOF simulation.
        maneuvering_params (Mmg3DofManeuveringParams):
            Maneuvering parameters for MMG 3DOF simulation.
        R_0_func (scipy.interpolate.interp1d):
            R_0 function which input value is `u`.
        time_list (list[float]):
            time list of simulation.
        delta_list (list[float]):
            rudder angle list of simulation.
        npm_list (List[float]):
            npm list of simulation.
        u0 (float, optional):
            axial velocity [m/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        v0 (float, optional):
            lateral velocity [m/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        r0 (float, optional):
            rate of turn [rad/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        ρ (float, optional):
            seawater density [kg/m^3]
            Defaults to 1.025.

    Returns:
        numpy.ndarray:
            The result of MMG 3DOF simulation.
            shape = (time, num_of_results)
            num_of_results = 5 including :math:`u`, :math:`v`, :math:`r`, :math:`\\delta` and npm.

    Note:
        For more information, please see the following articles.

        - Yasukawa, H., Yoshimura, Y. (2015) Introduction of MMG standard method for ship maneuvering predictions.
          J Mar Sci Technol 20, 37–52 https://doi.org/10.1007/s00773-014-0293-y

    """
    return simulate(
        L_pp=basic_params.L_pp,
        B=basic_params.B,
        d=basic_params.d,
        nabla=basic_params.nabla,
        x_G=basic_params.x_G,
        D_p=basic_params.D_p,
        m_=basic_params.m_,
        I_zG=basic_params.I_zG,
        Λ=basic_params.Λ,
        A_R_Ld=basic_params.A_R_Ld,
        η=basic_params.η,
        m_x_=basic_params.m_x_,
        m_y_=basic_params.m_y_,
        J_z=basic_params.J_z,
        f_α=basic_params.f_α,
        ϵ=basic_params.ϵ,
        t_R=basic_params.t_R,
        a_H=basic_params.a_H,
        x_H=basic_params.x_H,
        γ_R=basic_params.γ_R,
        l_R=basic_params.l_R,
        κ=basic_params.κ,
        t_P=basic_params.t_P,
        w_P0=basic_params.w_P0,
        C_1=maneuvering_params.C_1,
        C_2=maneuvering_params.C_2,
        C_3=maneuvering_params.C_3,
        X_0=maneuvering_params.X_0,
        X_ββ=maneuvering_params.X_ββ,
        X_βγ=maneuvering_params.X_βγ,
        X_γγ=maneuvering_params.X_γγ,
        X_ββββ=maneuvering_params.X_ββββ,
        Y_β=maneuvering_params.Y_β,
        Y_γ=maneuvering_params.Y_γ,
        Y_βββ=maneuvering_params.Y_βββ,
        Y_ββγ=maneuvering_params.Y_ββγ,
        Y_βγγ=maneuvering_params.Y_βγγ,
        Y_γγγ=maneuvering_params.Y_γγγ,
        N_β=maneuvering_params.N_β,
        N_γ=maneuvering_params.N_γ,
        N_βββ=maneuvering_params.N_βββ,
        N_ββγ=maneuvering_params.N_ββγ,
        N_βγγ=maneuvering_params.N_βγγ,
        N_γγγ=maneuvering_params.N_γγγ,
        R_0_func=R_0_func,
        time_list=time_list,
        delta_list=delta_list,
        npm_list=npm_list,
        u0=u0,
        v0=v0,
        r0=r0,
        ρ=ρ,
    )


def simulate(
    L_pp: float,
    B: float,
    d: float,
    nabla: float,
    x_G: float,
    D_p: float,
    m_: float,
    I_zG: float,
    Λ: float,
    A_R_Ld: float,
    η: float,
    m_x_: float,
    m_y_: float,
    J_z: float,
    f_α: float,
    ϵ: float,
    t_R: float,
    a_H: float,
    x_H: float,
    γ_R: float,
    l_R: float,
    κ: float,
    t_P: float,
    w_P0: float,
    C_1: float,
    C_2: float,
    C_3: float,
    X_0: float,
    X_ββ: float,
    X_βγ: float,
    X_γγ: float,
    X_ββββ: float,
    Y_β: float,
    Y_γ: float,
    Y_βββ: float,
    Y_ββγ: float,
    Y_βγγ: float,
    Y_γγγ: float,
    N_β: float,
    N_γ: float,
    N_βββ: float,
    N_ββγ: float,
    N_βγγ: float,
    N_γγγ: float,
    R_0_func: interp1d,
    time_list: List[float],
    delta_list: List[float],
    npm_list: List[float],
    u0: float = 0.0,
    v0: float = 0.0,
    r0: float = 0.0,
    ρ: float = 1.025,
):
    """MMG 3DOF simulation
    MMG 3DOF simulation by follwoing equation of motion.

    .. math::

        m (\dot{u}-vr)&=-m_x\dot{u}+m_yvr+X_H+R_0+X_P+X_R

        m (\dot{v}+ur)&=-m_y\dot{v}+m_xur+Y_H+Y_R

        I_{zG}\dot{r}&=-J_Z\dot{r}+N_H+N_R

    Args:
        L_pp (float):
            Ship length between perpendiculars [m]
        B (float):
            Ship breadth [m]
        d (float):
            Ship draft [m]
        nabla (float):
            Displacement volume of ship [m^3]
        x_G (float):
            Longitudinal coordinate of center of gravity of ship [-]
        D_p (float):
            Propeller diameter [m]
        m_ (float):
            Ship mass (non-dimensionalized) [-]
        I_zG (float):
            Moment of inertia of ship around center of gravity [-]
        Λ (float):
            Rudder aspect ratio [-]
        A_R_Ld (float):
            Profile area of movable part of mariner rudder[-]
        η (float):
            Ratio of propeller diameter to rudder span (=D_p/HR)
        m_x_ (float):
            Added masses of x axis direction (non-dimensionalized)
        m_y_ (float):
            Added masses of y axis direction (non-dimensionalized)
        J_z (float):
            Added moment of inertia (non-dimensionalized)
        f_α (float):
            Rudder lift gradient coefficient
        ϵ (float):
            Ratio of wake fraction at propeller and rudder positions
        t_R (float):
            Steering resistance deduction factor
        a_H (float):
            Rudder force increase factor
        x_H (float):
            Longitudinal coordinate of acting point of the additional lateral force component induced by steering
        γ_R (float):
            Flow straightening coefficient
        l_R (float):
            Effective longitudinal coordinate of rudder position in formula of βR
        κ (float):
            An experimental constant for　expressing uR
        t_P (float):
            Thrust deduction factor
        w_P0 (float):
            Wake coefficient at propeller position in straight moving
        C_1 (float):
            One of manuevering parameters of MMG 3DOF
        C_2 (float):
            One of manuevering parameters of MMG 3DOF
        C_3 (float):
            One of manuevering parameters of MMG 3DOF
        X_0 (float):
            One of manuevering parameters of MMG 3DOF
        X_ββ (float):
            One of manuevering parameters of MMG 3DOF
        X_βγ (float):
            One of manuevering parameters of MMG 3DOF
        X_γγ (float):
            One of manuevering parameters of MMG 3DOF
        X_ββββ (float):
            One of manuevering parameters of MMG 3DOF
        Y_β (float):
            One of manuevering parameters of MMG 3DOF
        Y_γ (float):
            One of manuevering parameters of MMG 3DOF
        Y_βββ (float):
            One of manuevering parameters of MMG 3DOF
        Y_ββγ (float):
            One of manuevering parameters of MMG 3DOF
        Y_βγγ (float):
            One of manuevering parameters of MMG 3DOF
        Y_γγγ (float):
            One of manuevering parameters of MMG 3DOF
        N_β (float):
            One of manuevering parameters of MMG 3DOF
        N_γ (float):
            One of manuevering parameters of MMG 3DOF
        N_βββ (float):
            One of manuevering parameters of MMG 3DOF
        N_ββγ (float):
            One of manuevering parameters of MMG 3DOF
        N_βγγ (float):
            One of manuevering parameters of MMG 3DOF
        N_γγγ (float):
            One of manuevering parameters of MMG 3DOF
        R_0_func (scipy.interpolate.interp1d):
            R_0 function which input value is `u`.
        time_list (list[float]):
            time list of simulation.
        delta_list (list[float]):
            rudder angle list of simulation.
        npm_list (List[float]):
            npm list of simulation.
        u0 (float, optional):
            axial velocity [m/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        v0 (float, optional):
            lateral velocity [m/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        r0 (float, optional):
            rate of turn [rad/s] in initial condition (`time_list[0]`).
            Defaults to 0.0.
        ρ (float, optional):
            seawater density [kg/m^3]
            Defaults to 1.025.

    Returns:
        numpy.ndarray:
            The result of MMG 3DOF simulation.
            shape = (time, num_of_params)
            num_of_params = 5 including :math:`u`, :math:`v`, :math:`r`, :math:`\\delta` and npm.

    Note:
        For more information, please see the following articles.

        - Yasukawa, H., Yoshimura, Y. (2015) Introduction of MMG standard method for ship maneuvering predictions.
          J Mar Sci Technol 20, 37–52 https://doi.org/10.1007/s00773-014-0293-y

    """
    spl_delta = interp1d(time_list, delta_list, "cubic", fill_value="extrapolate")
    spl_npm = interp1d(time_list, npm_list, "cubic", fill_value="extrapolate")

    def mmg_3dof_eom(X, t):

        U = np.sqrt(X[0] ** 2 + (X[1] - X[2] * x_G) ** 2)
        β = 0.0 if U == 0.0 else np.arcsin(-(X[1] - X[2] * x_G) / U)

        γ_dash = 0.0 if U == 0.0 else X[2] * L_pp / U
        J = 0.0 if X[4] == 0.0 else (1 - w_P0) * X[0] / (X[4] * D_p)
        K_T = C_1 + C_2 * J + C_3 * J ** 2
        v_R = U * γ_R * (np.sin(β) - l_R * γ_dash)
        u_R = (
            np.sqrt(η * (κ * ϵ * 8.0 * C_1 * X[4] ** 2 * D_p ** 4 / np.pi) ** 2)
            if J == 0.0
            else X[0]
            * (1 - w_P0)
            * ϵ
            * np.sqrt(
                η * (1.0 + κ * (np.sqrt(1.0 + 8.0 * K_T / (np.pi * J ** 2)) - 1)) ** 2
                + (1 - η)
            )
        )
        U_R = np.sqrt(u_R ** 2 + v_R ** 2)
        α_R = X[3] - np.arctan2(v_R, u_R)
        F_N = A_R_Ld * f_α * (U_R ** 2) * np.sin(α_R)

        X_H = (
            0.5
            * ρ
            * L_pp
            * d
            * (U ** 2)
            * (
                X_0
                + X_ββ * β ** 2
                + X_βγ * β * γ_dash
                + X_γγ * γ_dash ** 2
                + X_ββββ * β ** 4
            )
        )
        R_0 = R_0_func(X[0])
        X_R = -(1 - t_R) * F_N * np.sin(X[3]) / L_pp
        X_P = (1 - t_P) * ρ * K_T * X[4] ** 2 * D_p ** 4 * (2 / (ρ * d * L_pp ** 2))
        Y_H = (
            0.5
            * ρ
            * L_pp
            * d
            * (U ** 2)
            * (
                Y_β * β
                + Y_γ * γ_dash
                + Y_ββγ * (β ** 2) * γ_dash
                + Y_βγγ * β * (γ_dash ** 2)
                + Y_βββ * (β ** 3)
                + Y_γγγ * (γ_dash ** 3)
            )
        )
        Y_R = -(1 + a_H) * F_N * np.cos(X[3]) / L_pp
        N_H = (
            0.5
            * ρ
            * (L_pp ** 2)
            * d
            * (U ** 2)
            * (
                N_β * β
                + N_γ * γ_dash
                + N_ββγ * (β ** 2) * γ_dash
                + N_βγγ * β * (γ_dash ** 2)
                + N_βββ * (β ** 3)
                + N_γγγ * (γ_dash ** 3)
            )
        )
        N_R = -(-0.5 + a_H * x_H) * F_N * np.cos(X[3]) / L_pp ** 2
        d_u = ((X_H - R_0 + X_R + X_P) + (m_ + m_y_) * X[1] * X[2]) / (m_ + m_x_)
        d_v = ((Y_H + Y_R) - (m_ + m_x_) * X[0] * X[2]) / (m_ + m_y_)
        d_r = (N_H + N_R) / (I_zG + J_z)
        d_δ = derivative(spl_delta, t)
        d_npm = derivative(spl_npm, t)
        return [d_u, d_v, d_r, d_δ, d_npm]

    X_init = np.array([u0, v0, r0, delta_list[0], npm_list[0]])
    X_result = odeint(mmg_3dof_eom, X_init, time_list)
    return X_result
