const form = document.getElementById('calc-form');
const resultsEl = document.getElementById('results');

function num(v) {
  return Number.parseFloat(v);
}

function renderResults(data) {
  resultsEl.innerHTML = `
    <ul>
      <li>Velocity: <strong>${data.velocity.toFixed(4)}</strong> m/s</li>
      <li>Reynolds: <strong>${data.reynolds.toFixed(0)}</strong></li>
      <li>Regime: <strong>${data.regime}</strong></li>
      <li>Relative roughness ε/D: <strong>${data.relative_roughness.toFixed(6)}</strong></li>
      <li>Darcy friction factor: <strong>${data.friction_factor.toFixed(5)}</strong></li>
      <li>Pressure drop ΔP: <strong>${data.pressure_drop.toFixed(2)}</strong> Pa</li>
      <li>Head loss: <strong>${data.head_loss.toFixed(4)}</strong> m</li>
    </ul>
  `;
}

async function submitForm(event) {
  event.preventDefault();
  const fd = new FormData(form);
  const payload = {
    flow_rate: num(fd.get('flow_rate')),
    diameter: num(fd.get('diameter')),
    length: num(fd.get('length')),
    roughness: num(fd.get('roughness')),
    density: num(fd.get('density')),
    viscosity: num(fd.get('viscosity')),
    method: String(fd.get('method')),
  };

  const res = await fetch('/api/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    resultsEl.innerHTML = `<p class="error">Gagal hitung: ${res.status} ${res.statusText}</p>`;
    return;
  }

  const data = await res.json();
  renderResults(data);
  Plotly.newPlot('moody-chart', data.plot.data, data.plot.layout, { responsive: true });
}

form.addEventListener('submit', submitForm);
form.dispatchEvent(new Event('submit'));
