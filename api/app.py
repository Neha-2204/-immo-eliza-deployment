from fastapi import FastAPI
from predict import predict

from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="Immo Eliza Price Prediction API")


class PropertyData(BaseModel):
    # Required — the model needs these to give a meaningful estimate
    bedrooms: int
    living_area_m2: float
    property_type: str
    province: str

    # Optional — pipeline imputes these if missing
    bathrooms: Optional[float] = None
    total_area_m2: Optional[float] = None
    facades: Optional[int] = None
    has_garage: Optional[int] = None
    has_garden: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state_of_the_building: Optional[str] = None
    epc_score: Optional[str] = None
    has_elevator: Optional[int] = None
    parking_count: Optional[int] = None
    garden_area_m2: Optional[float] = None
    is_nearby_city_prestigious: Optional[int] = None
    kitchen_equipped: Optional[str] = None
    building_year: Optional[int] = None

class PredictionInput(BaseModel):
    data: PropertyData


class PredictionOutput(BaseModel):
    prediction: Optional[float] = None
    status_code: int


@app.get("/")           #whenever someone sends a GET request to the / path, run the function right below me
def read_root():
    """Health check route."""
    return "alive"        # FastAPI automatically converts whatever you return into JSON.

@app.post("/predict", response_model=PredictionOutput)
def get_prediction(input: PredictionInput):
    """Takes property data as JSON and returns the predicted price."""
    try:
        price = predict(input.data.model_dump())
        return PredictionOutput(prediction=price, status_code=200)
    except Exception as e:
        print(f"Prediction error: {e}")
        return PredictionOutput(prediction=None, status_code=500)