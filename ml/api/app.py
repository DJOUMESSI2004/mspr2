from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="API Prédiction COVID-19 - Nouveaux Cas")

# Middleware CORS pour la gestion des requêtes cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle
model = joblib.load("../model/rf_model_canada.joblib")

# Schéma d'entrée API
class PredictionInput(BaseModel):
    new_cases_lag1: float
    new_cases_lag7: float
    new_cases_ma7: float
    growth_rate: float
    reproduction_rate: float
    positive_rate: float
    icu_patients: float
    hosp_patients: float
    stringency_index: float
    vaccinated_rate: float
    boosted_rate: float

@app.post("/predict")
def predict_cases(input: PredictionInput):
    features = np.array([[
        input.new_cases_lag1,
        input.new_cases_lag7,
        input.new_cases_ma7,
        input.growth_rate,
        input.reproduction_rate,
        input.positive_rate,
        input.icu_patients,
        input.hosp_patients,
        input.stringency_index,
        input.vaccinated_rate,
        input.boosted_rate
    ]])
    prediction = model.predict(features)[0]
    return {"predicted_new_cases": round(float(prediction), 2)}

# Interface HTML simple pour la prédiction des nouveaux cas COVID-19
@app.get("/", response_class=HTMLResponse)
async def form_get():
    return '''
    <html>
    <head>
        <title>Prédiction COVID-19</title>
    </head>
    <body>
        <h2>Formulaire de prédiction des nouveaux cas COVID-19</h2>
        <form action="/form_predict" method="post">
            ''' + "".join([f'{name}: <input type="number" step="any" name="{name}" required><br><br>' for name in [
                "new_cases_lag1", "new_cases_lag7", "new_cases_ma7", "growth_rate",
                "reproduction_rate", "positive_rate", "icu_patients", "hosp_patients",
                "stringency_index", "vaccinated_rate", "boosted_rate"
            ]]) + '''
            <input type="submit" value="Prédire">
        </form>
    </body>
    </html>
    '''
# Formulaire de prédiction des nouveaux cas COVID-19
@app.post("/form_predict", response_class=HTMLResponse)
async def form_predict(
    new_cases_lag1: float = Form(...),
    new_cases_lag7: float = Form(...),
    new_cases_ma7: float = Form(...),
    growth_rate: float = Form(...),
    reproduction_rate: float = Form(...),
    positive_rate: float = Form(...),
    icu_patients: float = Form(...),
    hosp_patients: float = Form(...),
    stringency_index: float = Form(...),
    vaccinated_rate: float = Form(...),
    boosted_rate: float = Form(...)
):
    features = np.array([[
        new_cases_lag1, new_cases_lag7, new_cases_ma7, growth_rate,
        reproduction_rate, positive_rate, icu_patients, hosp_patients,
        stringency_index, vaccinated_rate, boosted_rate
    ]])
    prediction = model.predict(features)[0]
    return f"<h2>Résultat : {round(prediction, 2)} nouveaux cas prédits</h2>"
