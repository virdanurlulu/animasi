"""Moody chart builder using Plotly."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from core.friction import darcy_friction_factor


ROUGHNESS_CURVES = [
    0.0,
    1e-6,
    5e-6,
    1e-5,
    5e-5,
    1e-4,
    5e-4,
    1e-3,
    5e-3,
    1e-2,
    5e-2,
]


def build_moody_figure(reynolds_point: float | None = None, friction_point: float | None = None) -> go.Figure:
    re_values = np.logspace(np.log10(500), np.log10(1e8), 250)

    fig = go.Figure()

    for rr in ROUGHNESS_CURVES:
        f_values = [darcy_friction_factor(float(re), rr, method="haaland") for re in re_values]
        fig.add_trace(
            go.Scatter(
                x=re_values,
                y=f_values,
                mode="lines",
                name=f"ε/D={rr:g}",
                line={"width": 1.5},
            )
        )

    if reynolds_point and friction_point:
        fig.add_trace(
            go.Scatter(
                x=[reynolds_point],
                y=[friction_point],
                mode="markers",
                name="Operating point",
                marker={"size": 10, "symbol": "x"},
            )
        )

    fig.update_layout(
        title="Moody Chart (Darcy Friction Factor)",
        xaxis={"title": "Reynolds Number (Re)", "type": "log"},
        yaxis={"title": "Darcy Friction Factor (f)", "type": "log"},
        template="plotly_white",
        legend={"title": "Relative roughness"},
    )

    return fig
