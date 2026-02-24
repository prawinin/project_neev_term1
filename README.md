# Project Neev - Term 1 Public Build

This directory is a **separate Term 1-only version** of Project Neev for public sharing and college demo.

## Included features (Term 1 only)
- Plot image scan (computer vision)
- Compliance check (basic city rules)
- Cost estimation + bill of materials
- Simple Streamlit frontend

## Not included
- Generative design
- ML cost prediction
- 3D visualization
- Material recommendation engine
- DXF/PDF export
- India comprehensive datasets/routes

## Run (Linux)

```bash
cd project_neev_term1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python launcher_linux.py
```

Backend: http://127.0.0.1:8000

Frontend: http://127.0.0.1:8501

API docs: http://127.0.0.1:8000/docs
