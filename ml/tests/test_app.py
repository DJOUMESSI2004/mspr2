import sys
import os

# Ajout du chemin pour accéder à app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
import app

# 🎭 Mock simple des modèles
class DummyModel:
    def predict(self, X):
        return ["mock"]  # ou [1234] selon le endpoint

# Remplace les vrais modèles par des mocks
app.get_model_cas = lambda: DummyModel()
app.get_model_tendance = lambda: DummyModel()

client = TestClient(app.app)

def test_predict_cases():
    response = client.post("/canada/predict-cases", data={
        "new_cases_lag1": 500,
        "new_cases_lag7": 600,
        "new_cases_ma7": 550,
        "growth_rate": 1.05,
        "reproduction_rate": 1.1,
        "positive_rate": 0.15,
        "icu_patients": 50,
        "hosp_patients": 200,
        "stringency_index": 70.5,
        "vaccinated_rate": 65.0,
        "boosted_rate": 25.0
    })
    assert response.status_code == 200

def test_predict_tendance():
    response = client.post("/canada/predict-tendance", data={
        "new_cases_7d_avg": 500,
        "new_deaths_7d_avg": 50,
        "lag_1": 500,
        "lag_2": 480,
        "lag_7": 460,
        "month": 6,
        "day_of_week": 3,
        "reproduction_rate": 1.1,
        "people_vaccinated": 15000000,
        "stringency_index": 70.5
    })
    assert response.status_code == 200

def test_predict_all():
    response = client.post("/canada/predict-all", data={
        "new_cases_lag1": 500,
        "new_cases_lag7": 600,
        "new_cases_ma7": 550,
        "reproduction_rate": 1.1,
        "positive_rate": 0.15,
        "icu_patients": 50,
        "hosp_patients": 200,
        "stringency_index": 70.5,
        "vaccinated_rate": 65.0,
        "boosted_rate": 25.0,
        "new_cases_7d_avg": 500,
        "new_deaths_7d_avg": 50,
        "lag_1": 500,
        "lag_2": 480,
        "lag_7": 460,
        "month": 6,
        "day_of_week": 3,
        "people_vaccinated": 15000000
    })
    assert response.status_code == 200
