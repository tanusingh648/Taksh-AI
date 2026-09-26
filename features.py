from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter()


@router.post("/features")
async def engineer_features(file: UploadFile = File(...)):

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))

    else:
        return {
            "error": "Only CSV and XLSX files are supported"
        }

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    feature_summary = {}

    for column in numerical_columns:
        feature_summary[column] = {
            "type": "numerical",
            "action": "ready_for_scaling"
        }

    for column in categorical_columns:
        feature_summary[column] = {
            "type": "categorical",
            "action": "needs_encoding"
        }

    return {
        "filename": file.filename,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numerical_features": numerical_columns,
        "categorical_features": categorical_columns,
        "feature_summary": feature_summary,
        "status": "Feature analysis completed"
    }
