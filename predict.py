from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import json
import os
import pandas as pd

router = APIRouter()

MODEL_DIR = "models"


class PredictionRequest(BaseModel):
    model_name: str
    data: dict


@router.post("/predict")
async def predict(request: PredictionRequest):

    model_name = request.model_name

    model_path = os.path.join(
        MODEL_DIR,
        model_name
    )

    metadata_name = (
        os.path.splitext(model_name)[0]
        + "_metadata.json"
    )

    metadata_path = os.path.join(
        MODEL_DIR,
        metadata_name
    )

    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    if not os.path.exists(metadata_path):
        raise HTTPException(
            status_code=404,
            detail="Model metadata not found. Retrain the model first."
        )

    model = joblib.load(model_path)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    feature_columns = metadata["feature_columns"]

    missing_features = [
        column
        for column in feature_columns
        if column not in request.data
    ]

    if missing_features:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Missing required features",
                "missing_features": missing_features
            }
        )

    input_data = {
        column: [request.data[column]]
        for column in feature_columns
    }

    input_df = pd.DataFrame(input_data)

    prediction = model.predict(input_df)

    return {
        "model": model_name,
        "problem_type": metadata["problem_type"],
        "target_column": metadata["target_column"],
        "prediction": prediction.tolist(),
        "status": "Prediction completed successfully"
    }
