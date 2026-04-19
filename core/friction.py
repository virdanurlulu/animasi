"""Darcy friction factor correlations and utilities."""

from __future__ import annotations

import math


def flow_regime(reynolds: float) -> str:
    if reynolds < 2000:
        return "laminar"
    if reynolds <= 4000:
        return "transitional"
    return "turbulent"


def friction_laminar(reynolds: float) -> float:
    if reynolds <= 0:
        raise ValueError("reynolds must be > 0")
    return 64.0 / reynolds


def friction_haaland(reynolds: float, rel_roughness: float) -> float:
    if reynolds <= 0:
        raise ValueError("reynolds must be > 0")
    if rel_roughness < 0:
        raise ValueError("rel_roughness must be >= 0")

    term = (rel_roughness / 3.7) ** 1.11 + 6.9 / reynolds
    return 1.0 / (-1.8 * math.log10(term)) ** 2


def friction_swamee_jain(reynolds: float, rel_roughness: float) -> float:
    if reynolds <= 0:
        raise ValueError("reynolds must be > 0")
    if rel_roughness < 0:
        raise ValueError("rel_roughness must be >= 0")

    return 0.25 / (math.log10(rel_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2)


def friction_colebrook(
    reynolds: float,
    rel_roughness: float,
    *,
    tol: float = 1e-8,
    max_iter: int = 100,
) -> float:
    """Solve Colebrook-White by fixed-point iteration.

    1/sqrt(f) = -2log10( (e/D)/3.7 + 2.51/(Re*sqrt(f)) )
    """
    if reynolds <= 0:
        raise ValueError("reynolds must be > 0")
    if rel_roughness < 0:
        raise ValueError("rel_roughness must be >= 0")

    if reynolds < 2000:
        return friction_laminar(reynolds)

    # Robust initial guess.
    f = friction_haaland(reynolds, rel_roughness)

    for _ in range(max_iter):
        left = -2.0 * math.log10(rel_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(f)))
        f_new = 1.0 / (left**2)
        if abs(f_new - f) < tol:
            return f_new
        f = f_new

    return f


def darcy_friction_factor(reynolds: float, rel_roughness: float, method: str = "colebrook") -> float:
    regime = flow_regime(reynolds)
    if regime == "laminar":
        return friction_laminar(reynolds)

    methods = {
        "colebrook": friction_colebrook,
        "haaland": friction_haaland,
        "swamee-jain": friction_swamee_jain,
    }
    if method not in methods:
        raise ValueError(f"Unknown method: {method}")
    return methods[method](reynolds, rel_roughness)
