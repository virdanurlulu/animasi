# Animasi
Explosion Animation Effected to building structure

Repository ini berisi **Moody Chart Tool** untuk engineering mechanical fluida dengan:
- **Backend Python** (menggunakan modul core yang sudah dibuat).
- **Web UI** (HTML/CSS/JS) yang memanggil API backend.

## Fitur
- Hitung kecepatan aliran, Reynolds number, flow regime.
- Hitung **Darcy friction factor** (laminar + Colebrook/Haaland/Swamee-Jain).
- Hitung pressure drop dengan persamaan Darcy–Weisbach.
- Tampilkan Moody chart interaktif di UI web.

## Menjalankan versi Web UI (disarankan)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

Buka di browser:
- http://127.0.0.1:8000

## Menjalankan Streamlit (opsional)
```bash
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

## Menjalankan test
```bash
pytest -q
```

## Struktur utama
- `server.py`: backend API FastAPI + serve Web UI.
- `web/`: frontend web (HTML/CSS/JS).
- `app.py`: antarmuka Streamlit (opsional).
- `core/`: kalkulasi inti fluida/friction/pressure drop.
- `charts/`: generator Moody chart.
- `tests/`: validasi dasar perhitungan.
