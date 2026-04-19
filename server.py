from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from charts.moody_plot import build_moody_figure
from core.fluids import reynolds_number, velocity_from_flowrate
from core.friction import darcy_friction_factor, flow_regime
from core.pressure_drop import head_loss_m, pressure_drop_pa


class CalculationRequest(BaseModel):
    flow_rate: float = Field(gt=0)
    diameter: float = Field(gt=0)
    length: float = Field(gt=0)
    roughness: float = Field(ge=0)
    density: float = Field(gt=0)
    viscosity: float = Field(gt=0)
    method: str = Field(default="colebrook")


app = FastAPI(title="Moody Chart Engineering API")
app.mount("/web", StaticFiles(directory="web"), name="web")


@app.get("/")
def index() -> FileResponse:
    return FileResponse("web/index.html")


@app.post("/api/calculate")
def calculate(payload: CalculationRequest) -> dict:
    velocity = velocity_from_flowrate(payload.flow_rate, payload.diameter)
    reynolds = reynolds_number(
        velocity,
        payload.diameter,
        density_kg_m3=payload.density,
        dynamic_viscosity_pa_s=payload.viscosity,
    )

    rel_roughness = payload.roughness / payload.diameter
    friction = darcy_friction_factor(reynolds, rel_roughness, method=payload.method)

    d_p = pressure_drop_pa(friction, payload.length, payload.diameter, payload.density, velocity)
    h_l = head_loss_m(d_p, payload.density)
    regime = flow_regime(reynolds)

    fig = build_moody_figure(reynolds, friction)

    return {
        "velocity": velocity,
        "reynolds": reynolds,
        "regime": regime,
        "relative_roughness": rel_roughness,
        "friction_factor": friction,
        "pressure_drop": d_p,
        "head_loss": h_l,
        "plot": fig.to_plotly_json(),
    }
