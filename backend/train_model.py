import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

# Get the project folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset path
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "house_data.csv")

# Model path
MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "house_model.pkl"
)

# Load dataset
data = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print(data)

# Input features
X = data[[
    "area",
    "bedrooms",
    "bathrooms",
    "age"
]]

# Target/output
y = data["price"]

# Create Linear Regression model
model = LinearRegression()

# Train model
model.fit(X, y)

# Save model
with open(MODEL_PATH, "wb") as file:
    pickle.dump(model, file)

print("\nModel trained successfully!")
print("Model saved at:", MODEL_PATH)

# Display coefficients
print("\nIntercept:", model.intercept_)
print("Coefficients:", model.coef_)