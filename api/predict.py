"""
predict.py — loads the trained pipeline from train.py and predicts price
for new property data.
"""

import os
import pandas as pd
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "best_model.joblib")

FEATURES = [
    "bedrooms", "bathrooms", "living_area_m2", "total_area_m2", "facades",
    "has_garage", "has_garden", "latitude", "longitude",
    "property_type", "province", "state_of_the_building", "epc_score",
    "has_elevator", "parking_count", "garden_area_m2", "is_nearby_city_prestigious",
    "kitchen_equipped","building_year"
]


def load_model(model_path: str = MODEL_PATH):
    """Loads the saved preprocessing+model pipeline."""
    try:
        pipeline = joblib.load(model_path)
        return pipeline
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
    
    
def preprocess(input_data: dict) -> pd.DataFrame:
    """
    Converts incoming JSON data into a DataFrame with the correct columns,
    in the order the model expects. Missing optional fields become None,
    which the pipeline's imputers handle.
    """
    row = {feature: input_data.get(feature) for feature in FEATURES}
    return pd.DataFrame([row])


def predict(input_data:dict) -> float:
      """
    Main prediction function used by FastAPI.
    Takes a single property (dict) and returns a float prediction.
    """
      pipeline = load_model()
      df = preprocess(input_data)
      prediction = pipeline.predict(df)[0]
      return float(prediction)


if __name__ == "__main__":
    example = {
            "bedrooms": 4, "bathrooms": 1, "living_area_m2": 194,
            "total_area_m2": 200, "facades": 3, "has_garage": 1,
            "has_garden": 1, "latitude": 51.18417, "longitude": 3.10000,
            "property_type": "House", "province": "Flanders",
            "state_of_the_building": "Excellent", "epc_score": "A",
            "has_elevator": 0, "parking_count": 2, "garden_area_m2": 100,
            "is_nearby_city_prestigious": 1,"kitchen_equipped":"Fully equipped",
            "building_year":2025,
        }
       

    price = predict(example)
    print(f"Predicted price = {price:,.2f} EUR")
