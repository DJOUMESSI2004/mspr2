# 🚀 FastAPI – API complète : nouveaux cas, tendance et /predict-all

from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI(title="API COVID-19 – Modèles IA (Canada)")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des modèles
model_cas = joblib.load("model/model_xgboost_covid.pkl")
model_tendance = joblib.load("model/modele_tendance_covid_rf.pkl")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("template.html", {"request": request})

# Prédiction des nouveaux cas
@app.post("/canada/predict-cases", response_class=HTMLResponse)
async def predict_cases(
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
    X = np.array([[
        new_cases_lag1, new_cases_lag7, new_cases_ma7, growth_rate,
        reproduction_rate, positive_rate, icu_patients, hosp_patients,
        stringency_index, vaccinated_rate, boosted_rate
    ]])
    try:
        y_pred = model_cas.predict(X)[0]
        return templates.TemplateResponse("template.html", {
            "request": request,
            "prediction": round(y_pred, 0),
            "type": "cas"
        })
    except Exception as e:
        return templates.TemplateResponse("template.html", {"request": request, "prediction": None, "error": str(e)})

# Prédiction de tendance
@app.post("/canada/predict-tendance", response_class=HTMLResponse)
async def predict_tendance(
    request: Request,
    new_cases_7d_avg: float = Form(...),
    new_deaths_7d_avg: float = Form(...),
    lag_1: float = Form(...),
    lag_2: float = Form(...),
    lag_7: float = Form(...),
    month: int = Form(...),
    day_of_week: int = Form(...),
    reproduction_rate: float = Form(...),
    people_vaccinated: float = Form(...),
    stringency_index: float = Form(...)
):
    X = np.array([[
        new_cases_7d_avg, new_deaths_7d_avg,
        lag_1, lag_2, lag_7, month, day_of_week,
        reproduction_rate, people_vaccinated, stringency_index
    ]])
    try:
        y_pred = model_tendance.predict(X)[0]
        return templates.TemplateResponse("template.html", {
            "request": request,
            "prediction": y_pred,
            "type": "tendance"
        })
    except Exception as e:
        return templates.TemplateResponse("template.html", {"request": request, "prediction": None, "error": str(e)})

@app.post("/canada/predict-all")
async def predict_all(
    request: Request,
    new_cases_lag1: float = Form(...),
    new_cases_lag7: float = Form(...),
    new_cases_ma7: float = Form(...),
    reproduction_rate: float = Form(...),
    positive_rate: float = Form(...),
    icu_patients: float = Form(...),
    hosp_patients: float = Form(...),
    stringency_index: float = Form(...),
    vaccinated_rate: float = Form(...),
    boosted_rate: float = Form(...),
    new_cases_7d_avg: float = Form(...),
    new_deaths_7d_avg: float = Form(...),
    lag_1: float = Form(...),
    lag_2: float = Form(...),
    lag_7: float = Form(...),
    month: int = Form(...),
    day_of_week: int = Form(...),
    people_vaccinated: float = Form(...)
):
    try:
        # Prédiction du nombre de cas
        X_cas = np.array([[
            new_cases_lag1, new_cases_lag7, new_cases_ma7,
            reproduction_rate, positive_rate, icu_patients, hosp_patients,
            stringency_index, vaccinated_rate, boosted_rate
        ]])
        pred_cas = model_cas.predict(X_cas)[0]

        # Prédiction de la tendance
        X_tendance = np.array([[
            new_cases_7d_avg, new_deaths_7d_avg, lag_1, lag_2, lag_7,
            month, day_of_week, reproduction_rate,
            people_vaccinated, stringency_index
        ]])
        pred_tendance = model_tendance.predict(X_tendance)[0]

        return templates.TemplateResponse("template.html", {
            "request": request,
            "prediction": f"{round(pred_cas)} cas / Tendance : {pred_tendance}",
            "type": "all"
        })

    except Exception as e:
        return templates.TemplateResponse("template.html", {
            "request": request,
            "prediction": None,
            "error": str(e)
        })
