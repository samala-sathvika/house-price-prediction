from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import os
import numpy as np

app = FastAPI(
    title="House Price Prediction API",
    description="Linear Regression House Price Prediction",
    version="1.0"
)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Find project folders
# -----------------------------

# backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# main project folder
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Model location
MODEL_PATH = os.path.join(BASE_DIR, "house_model.pkl")

# Frontend location
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")


# -----------------------------
# Load trained model
# -----------------------------

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


# -----------------------------
# Input data format
# -----------------------------

class HouseData(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    age: float


# -----------------------------
# API test endpoint
# -----------------------------

@app.get("/api")
def api_home():
    return {
        "message": "House Price Prediction API is running!"
    }


# -----------------------------
# Prediction endpoint
# -----------------------------

@app.post("/predict")
def predict_price(house: HouseData):

    # Prepare input for model
    input_data = np.array([[
        house.area,
        house.bedrooms,
        house.bathrooms,
        house.age
    ]])

    # Predict price
    prediction = model.predict(input_data)

    predicted_price = prediction[0]

    return {
        "predicted_price": round(float(predicted_price), 2)
    }


# -----------------------------
# Serve frontend
# -----------------------------

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)