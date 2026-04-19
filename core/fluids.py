"""Core fluid mechanics helpers."""

from __future__ import annotations

import math


def velocity_from_flowrate(flow_rate_m3_s: float, diameter_m: float) -> float:
    """Return average pipe velocity from volumetric flow rate.

    Args:
        flow_rate_m3_s: Volumetric flow rate [m^3/s].
        diameter_m: Internal diameter [m].
    """
    if diameter_m <= 0:
        raise ValueError("diameter_m must be > 0")
    area = math.pi * diameter_m**2 / 4.0
    return flow_rate_m3_s / area


def reynolds_number(
    velocity_m_s: float,
    diameter_m: float,
    *,
    kinematic_viscosity_m2_s: float | None = None,
    density_kg_m3: float | None = None,
    dynamic_viscosity_pa_s: float | None = None,
) -> float:
    """Calculate Reynolds number.

    Supports either kinematic viscosity (nu) directly, or rho+mu.
    """
    if diameter_m <= 0:
        raise ValueError("diameter_m must be > 0")

    if kinematic_viscosity_m2_s is None:
        if density_kg_m3 is None or dynamic_viscosity_pa_s is None:
            raise ValueError(
                "Provide either kinematic_viscosity_m2_s or both density_kg_m3 and dynamic_viscosity_pa_s"
            )
        if density_kg_m3 <= 0 or dynamic_viscosity_pa_s <= 0:
            raise ValueError("density_kg_m3 and dynamic_viscosity_pa_s must be > 0")
        kinematic_viscosity_m2_s = dynamic_viscosity_pa_s / density_kg_m3

    if kinematic_viscosity_m2_s <= 0:
        raise ValueError("kinematic_viscosity_m2_s must be > 0")

    return abs(velocity_m_s) * diameter_m / kinematic_viscosity_m2_s
