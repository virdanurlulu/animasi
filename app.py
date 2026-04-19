from __future__ import annotations

import streamlit as st

from charts.moody_plot import build_moody_figure
from core.fluids import reynolds_number, velocity_from_flowrate
from core.friction import darcy_friction_factor, flow_regime
from core.pressure_drop import head_loss_m, pressure_drop_pa

st.set_page_config(page_title="Moody Chart Tool", layout="wide")
st.title("Moody Chart — Mechanical Fluid Engineering")
st.caption("Darcy friction factor, Reynolds number, and pressure drop estimator.")

col1, col2 = st.columns(2)

with col1:
    flow_rate = st.number_input("Flow rate Q [m³/s]", min_value=0.0, value=0.02, step=0.001, format="%.6f")
    diameter = st.number_input("Pipe diameter D [m]", min_value=1e-6, value=0.1, step=0.001, format="%.6f")
    length = st.number_input("Pipe length L [m]", min_value=1e-6, value=30.0, step=1.0)
    roughness = st.number_input("Absolute roughness ε [m]", min_value=0.0, value=0.000045, format="%.6f")

with col2:
    density = st.number_input("Density ρ [kg/m³]", min_value=1e-6, value=998.2, step=1.0)
    viscosity = st.number_input("Dynamic viscosity μ [Pa·s]", min_value=1e-9, value=0.001003, format="%.6f")
    method = st.selectbox("Turbulent correlation", ["colebrook", "haaland", "swamee-jain"], index=0)

if flow_rate > 0 and diameter > 0:
    velocity = velocity_from_flowrate(flow_rate, diameter)
    reynolds = reynolds_number(velocity, diameter, density_kg_m3=density, dynamic_viscosity_pa_s=viscosity)
    rel_roughness = roughness / diameter
    friction = darcy_friction_factor(reynolds, rel_roughness, method=method)

    d_p = pressure_drop_pa(friction, length, diameter, density, velocity)
    h_l = head_loss_m(d_p, density)
    regime = flow_regime(reynolds)

    k1, k2, k3 = st.columns(3)
    k1.metric("Velocity [m/s]", f"{velocity:.4f}")
    k2.metric("Reynolds number", f"{reynolds:.0f}")
    k3.metric("Regime", regime)

    k4, k5, k6 = st.columns(3)
    k4.metric("Relative roughness ε/D", f"{rel_roughness:.6f}")
    k5.metric("Darcy friction factor f", f"{friction:.5f}")
    k6.metric("Pressure drop ΔP [Pa]", f"{d_p:.2f}")

    st.metric("Head loss [m]", f"{h_l:.4f}")

    if 2000 <= reynolds <= 4000:
        st.warning("Flow is in transitional regime (Re 2000–4000). Interpret friction factor cautiously.")

    st.plotly_chart(build_moody_figure(reynolds, friction), use_container_width=True)
else:
    st.info("Provide positive flow rate and diameter.")
