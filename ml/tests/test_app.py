import sys
import os
from unittest.mock import MagicMock
import pytest

# Ajouter le chemin pour importer app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📌 Monkeypatch joblib.load avant d'importer app.py
import joblib

def fake_load(path):
    class DummyModel:
        def predict(self, X):
            if "tendance" in path:
                return ["hausse"]
            return [1234]
    return DummyModel()

joblib.load = fake_load  # ⛔ intercepte le vrai chargement .pkl

# Maintenant on peut importer app sans que ça plante
import app
from fastapi.testclient import TestClient

client = TestClient(app.app)

def test_predict_cases():
    response = client.post("/canada/predict-cases", data={
        "new_cases_lag1": 100,
        "new_cases_lag7": 100,
        "new_cases_ma7": 100,
        "growth_rate": 1.0,
        "reproduction_rate": 1.0,
        "positive_rate": 0.1,
        "icu_patients": 20,
        "hosp_patients": 80,
        "stringency_index": 60.0,
        "vaccinated_rate": 50.0,
        "boosted_rate": 20.0
    })
    assert response.status_code == 200

def test_predict_tendance():
    response = client.post("/canada/predict-tendance", data={
        "new_cases_7d_avg": 100,
        "new_deaths_7d_avg": 5,
        "lag_1": 90,
        "lag_2": 80,
        "lag_7": 60,
        "month": 6,
        "day_of_week": 2,
        "reproduction_rate": 1.0,
        "people_vaccinated": 5000000,
        "stringency_index": 50.0
    })
    assert response.status_code == 200

def test_predict_all():
    response = client.post("/canada/predict-all", data={
        "new_cases_lag1": 100,
        "new_cases_lag7": 100,
        "new_cases_ma7": 100,
        "reproduction_rate": 1.0,
        "positive_rate": 0.1,
        "icu_patients": 20,
        "hosp_patients": 80,
        "stringency_index": 60.0,
        "vaccinated_rate": 50.0,
        "boosted_rate": 20.0,
        "new_cases_7d_avg": 100,
        "new_deaths_7d_avg": 5,
        "lag_1": 90,
        "lag_2": 80,
        "lag_7": 60,
        "month": 6,
        "day_of_week": 2,
        "people_vaccinated": 5000000
    })
    assert response.status_code == 200
