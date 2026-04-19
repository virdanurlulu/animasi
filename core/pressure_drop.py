"""Pressure drop calculations based on Darcy-Weisbach."""

from __future__ import annotations


def pressure_drop_pa(
    friction_factor: float,
    length_m: float,
    diameter_m: float,
    density_kg_m3: float,
    velocity_m_s: float,
) -> float:
    if min(friction_factor, length_m, diameter_m, density_kg_m3) <= 0:
        raise ValueError("friction_factor, length_m, diameter_m, density_kg_m3 must be > 0")
    return friction_factor * (length_m / diameter_m) * (density_kg_m3 * velocity_m_s**2 / 2.0)


def head_loss_m(pressure_drop_pa_value: float, density_kg_m3: float, g_m_s2: float = 9.80665) -> float:
    if density_kg_m3 <= 0:
        raise ValueError("density_kg_m3 must be > 0")
    return pressure_drop_pa_value / (density_kg_m3 * g_m_s2)
