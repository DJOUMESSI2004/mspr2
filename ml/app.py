from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="API Prédiction COVID-19 - Nouveaux Cas (Canada)")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle
model_canada = joblib.load("model/rf_model_canada.joblib")
model_any_country = joblib.load("model/rf_model_global.joblib")

# Configuration des templates
templates = Jinja2Templates(directory="templates")

# Page d’accueil avec formulaire (GET)
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("template.html", {"request": request, "prediction": None})

# Traitement du formulaire (POST) pour la prédiction des nouveaux cas au Canada
@app.post("/canada/new-cases", response_class=HTMLResponse)
async def form_predict(
    request: Request,
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
    prediction = model_canada.predict(features)[0]
    return templates.TemplateResponse("template.html", {
        "request": request,
        "prediction": round(prediction, 0) # Arrondi à l'entier le plus proche
    })