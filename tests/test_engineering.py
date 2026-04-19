from core.fluids import reynolds_number, velocity_from_flowrate
from core.friction import darcy_friction_factor, flow_regime
from core.pressure_drop import pressure_drop_pa


def test_velocity_and_reynolds_water_example() -> None:
    v = velocity_from_flowrate(0.01, 0.1)
    re = reynolds_number(v, 0.1, density_kg_m3=998.2, dynamic_viscosity_pa_s=0.001003)
    assert v > 0
    assert re > 10000


def test_laminar_factor() -> None:
    f = darcy_friction_factor(1000, 0.0, method="colebrook")
    assert abs(f - 0.064) < 1e-6


def test_regime_classification() -> None:
    assert flow_regime(1500) == "laminar"
    assert flow_regime(3000) == "transitional"
    assert flow_regime(8000) == "turbulent"


def test_pressure_drop_positive() -> None:
    dp = pressure_drop_pa(0.02, 10, 0.1, 1000, 2)
    assert dp > 0
