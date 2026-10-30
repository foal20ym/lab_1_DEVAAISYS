# Iris Predictor — Lab 1 starter project

A minimal **Flask + scikit-learn** application for the optional individual lab in *Developing AI-enabled Systems*. The trained classifier predicts one of three Iris species from four measurements in centimeters. The main learning goal is to practice Git, GitHub Issues, pull requests and automated testing, **not** to improve the ML model.

## Quick start

Python 3.10+ is required (Python 3.11 or 3.12 recommended).

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 and press **Predict**.

## Tests (already provided)

```bash
python -m pytest -v
```

`tests/test_app.py` contains two passing example tests: one valid prediction, one invalid request. You may extend them with your own tests. The task is to **create a GitHub Actions workflow yourself**; the starter intentionally contains no workflow YAML.

## API

`POST /predict` with JSON:

```json
{"measurements": [5.1, 3.5, 1.4, 0.2]}
```

A successful request returns JSON containing `species`. Bad input returns HTTP 400 with JSON containing `error`.

This is a teaching demo; do not use Flask debug mode outside local development.
