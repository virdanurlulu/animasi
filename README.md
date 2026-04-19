# Animasi

Repository ini sekarang berisi **MVP Moody Chart Tool** untuk kebutuhan engineering mechanical fluida.

## Fitur
- Hitung kecepatan aliran, Reynolds number, flow regime.
- Hitung **Darcy friction factor** (laminar + Colebrook/Haaland/Swamee-Jain).
- Hitung pressure drop dengan persamaan Darcy–Weisbach.
- Visualisasi Moody chart interaktif dengan titik operasi.

## Menjalankan aplikasi
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Menjalankan test
```bash
pytest -q
```

## Struktur utama
- `app.py`: antarmuka Streamlit.
- `core/`: kalkulasi inti fluida/friction/pressure drop.
- `charts/`: generator Moody chart.
- `tests/`: validasi dasar perhitungan.
