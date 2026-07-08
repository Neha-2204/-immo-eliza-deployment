from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import streamlit as st
import joblib

# --- Configuration ---
st.set_page_config(page_title="Price Predictor for Real Estate", layout="centered")

# --- Data Loading and Model Training ---
@st.cache_resource
def load_model():
    """Loads the model."""
    try:
        model = joblib.load("models\best_model.joblib")
        return model
        
    except FileNotFoundError:
        st.error("Error: 'best_model.joblib' not found. Please make sure it's in the same directory.")
        return None()
    

model = load_model()

st.title("Price Predictor for Real Estate")

if model is None:
    st.stop()

# --- Streamlit UI ---
st.title("Price Predictor for Properties")
st.write("This app uses **XGBoost** to predict a Properties's **Total Price** based on its **Features**.")
bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, value=1)
living_area = st.number_input("Living Area (m²)", min_value=10, max_value=1000, value=150)

input_df = pd.DataFrame([{
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "living_area_m2": living_area
}])

prediction = model.predict(input_df)[0]

st.success(f"Predicted price: €{prediction:,.2f}")